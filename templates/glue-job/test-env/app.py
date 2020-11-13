#!/usr/bin/env python3

from aws_cdk import core, aws_ec2, aws_redshift, aws_sam


class TestEnvStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        nat_instance = aws_ec2.NatProvider.instance(instance_type=aws_ec2.InstanceType('t3a.nano'))

        vpc = aws_ec2.Vpc(self, 'VPC',
                          max_azs=1,
                          nat_gateway_provider=nat_instance)

        cluster_security_group = aws_ec2.SecurityGroup(self, 'ClusterSecurityGroup',
                                                       vpc=vpc,
                                                       allow_all_outbound=True,
                                                       description="Allow Glue Job to access redshift",
                                                       security_group_name="serverless-redshift-query-testing-redshift")

        cluster = aws_redshift.Cluster(self, 'Cluster',
                                       cluster_name='serverless-redshift-query-testing',
                                       master_user=aws_redshift.Login(master_username='master'),
                                       vpc=vpc,
                                       removal_policy=core.RemovalPolicy.DESTROY,
                                       security_groups=[cluster_security_group])

        app = aws_sam.CfnApplication(self, 'RedshiftQueryGlueJob',
                                     location='https://redshift-query.s3-eu-west-1.amazonaws.com/glue-job-template.yaml',
                                     parameters={
                                         'ClusterId': 'serverless-redshift-query-testing',
                                         'SQLStatements': "select 1;",
                                         'Loglevel': "ERROR"
                                     })

        glue_job_security_group_ref = app.get_att('Outputs.SecurityGroup').to_string()
        glue_job_security_group = aws_ec2.SecurityGroup.from_security_group_id(self, 'GlueSecurityGroup',
                                                                               glue_job_security_group_ref)

        cluster_security_group.add_ingress_rule(
            peer=glue_job_security_group,
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.TCP,
                from_port=5439,
                to_port=5439,
                string_representation='Redshift Port'
            )
        )

        app.node.add_dependency(cluster)


env = core.Environment()

app = core.App()
TestEnvStack(app, "test-env", env=env)

app.synth()
