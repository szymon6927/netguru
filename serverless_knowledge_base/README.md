# serverless knowledge base

The main goal of this repository is to show all useful packages, tips, libraries 
which will help in python serverless (AWS Lambda) development in day to day basis. 

## Layers

During development in a serverless environment, it happens quite often that we need to share pieces of code 
between lambdas. As developers, we want to follow the DRY rule.

We have 3 options:
- duplicate the code in every lambda
- create our own package and install it as a dependency (mostly some internal package repository will be required)
- use a lambda layer


Here I would like to present a few interesting articles about lambda layers which should make the whole introduction process a little bit easier:
- <https://medium.com/@adhorn/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d>
- <https://medium.com/better-programming/how-to-build-both-kinds-of-aws-lambda-layers-yes-there-are-two-edb945979f17>
- <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>



*Additional note*

AWS offers a few pre-build layers, so eg. if you need `numpy` or `scipy` you can use a layer created by AWS:
<https://aws.amazon.com/blogs/aws/new-for-aws-lambda-use-any-programming-language-and-share-common-components/> 


## Debugging

#### python-lambda-local

[python-lambda-local](https://pypi.org/project/python-lambda-local/) allows you to debug your lambda functions
locally with eg. pycharm debugger.

Here is a great article with the whole explanation of how to use this package:
<https://medium.com/@bezdelev/how-to-test-a-python-aws-lambda-function-locally-with-pycharm-run-configurations-6de8efc4b206>


I would like to attach a simple snippet of python code which can be useful.

```python
from lambda_local import main
from os import chdir
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

if __name__ == '__main__':
    chdir(CURRENT_DIR)
    main()
```

Save above snippet as `.local_invoke.py`

To debug locally use script above which accepts same arguments as `sls invoke`.

In your IDE click Edit configuration add new Python configuration. 
Point Script Path to `.local_invoke.py` file, 
and in the Parameters add the following line `-f <path-to-your-lambda-handler-file> <path-to-your-exmaple-event-file>`
to debug function. Save configuration and click debug button.


## Testing

### moto

Personally, in my day to day basis I'm using [moto](https://github.com/spulec/moto) library, 
and I would recommend to use it in your project too. 
I know there are alternatives but in my opinion, this library is enough, 
besides that the usage is really simple and straight forward.


Let's start with examples:

#### s3

```python
import boto3
import pytest
import os

from moto import mock_s3

@pytest.fixture(scope="function")
def s3_bucket():
    with mock_s3():
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.create_bucket(Bucket=os.environ["BUCKET_NAME"])

        yield

        bucket.objects.all().delete()
        bucket.object_versions.delete()
        bucket.delete()
```

```python
import boto3
import pytest
import os

@pytest.mark.usefixtures("s3_bucket")
def test_file_upload(self):
    s3_client = boto3.client("s3")

    with open(f"{dir_path}/fixtures/your-dummy-file.csv") as f:
        s3_client.put_object(
            Body=f.read(),
            Bucket=os.environ["BUCKET_NAME"],
            Key="your-path/new-file.csv",
        )

    # do everything which you need in your test eg. check if file was correctly uploaded, correctly handled and so on.
```

#### sqs

```python
import boto3
import pytest
import os

from moto import mock_sqs

@pytest.fixture(scope="function")
def sqs_queue():
    with mock_sqs():
        sqs_client = boto3.client("sqs")
        response = sqs_client.create_queue(QueueName=os.environ["SQS_QUEUE_NAME"])
        queue_url = response["QueueUrl"]

        yield

        sqs_client.delete_queue(QueueUrl=queue_url)
```


#### secret manager

```python
import boto3
import pytest

from moto import mock_secretsmanager

@pytest.fixture(scope="function")
def secrets_manager():
    with mock_secretsmanager():
        secretsmanager_client = boto3.client("secretsmanager")

        secretsmanager_client.create_secret(
            Name="your-secrets-name",
            SecretString="your-secret-values",
        )

        yield
```

#### dynamodb

```python
import boto3
import pytest

from moto import mock_dynamodb2

@pytest.fixture(scope="function")
def dynamodb():
    with mock_dynamodb2():

        table_name = "your_table_name"
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        dynamodb_client = boto3.client("dynamodb", region_name="eu-west-1")

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[], # your db table key schema
            AttributeDefinitions=[], # your db table attribute definitions
            ProvisionedThroughput={"ReadCapacityUnits": 100, "WriteCapacityUnits": 100},
        )
        
        for item in <your_data_list>:
            table.put_item(Item=item)

        yield

        dynamodb_client.delete_table(TableName=table_name)
```

There are also a lot more AWS services that you can easily mock with moto like `moto` like: `sns, cloudwatch, cognitoidp`.


## Tools

During work in AWS environment, it happens very often to call services via API endpoint or call some service/command
with AWS permissions. I would like to show you two tools which 
are useful in above cases.


#### AWS Vault

[AWS Vault](https://github.com/99designs/aws-vault) - this is a tool which allows you to access multiple AWS credentials.

Tutorial how to add specific profiles is well described in the project documentation, lets start with real use cases.

If you have 3 different AWS environments with 3 different profiles for them for example :
```
staging
pre-prod
prod
```

and you want to call some AWS service eg. `s3` bucket to list elements you can easily call:
```
$ aws-vault exec <your-profile-specific-env> -- aws s3 ls
```

or for example if you want to call ECS task you can also use:
```
$ aws-vault exec <your-profile-specific-env> -- aws ecs run-task --task-definition <your-task-name> --overrides '{"containerOverrides": [{"name": "rico", "command": [your-task-params]}]}' --output text
```

So bascially you can any command from AWS SDK list with specific permission assigned to your profile.


#### awscurl

[awscurl](https://github.com/okigan/awscurl) 
use this tool if you need to request AWS API service with AWS Signature Version 4 request signing.

Examples:

If you want to call `API Gateway` service:
```
$ aws-vault exec <your-profile-specific-env> -- awscurl --service execute-api -X POST '<service-url>' -d '{<request-body>}' --region <service-region>
```


## Serverless framework plugins

In this section, I would like to show the most usable serverless frameworks plugins. 
The list will contain these which I think are the most useful.


#### [serverless-plugin-composed-vars](https://www.serverless.com/plugins/serverless-plugin-composed-vars/)

This plugin allows you to define custom variables for different stages/environments

#### [serverless-pseudo-parameters](https://www.npmjs.com/package/serverless-pseudo-parameters)

This plugin makes much easier usage of CloudFormation Pseudo Parameters in serverless.yml 

#### [serverless-domain-manager](https://www.npmjs.com/package/serverless-domain-manager)

Allows you to create custom domain names

#### [serverless-kms-grants](https://www.npmjs.com/package/serverless-kms-grants)

Use it when you want to use KMS key in your lambda.

#### [serverless-python-requirements](https://www.npmjs.com/package/serverless-python-requirements)

It makes python dependencies management much easier, based on `requirements.txt` the bundle will be
automatically generated.

Also it's worth to look at this blog post -> <https://www.serverless.com/blog/serverless-python-packaging/>

#### [serverless-iam-roles-per-function](https://www.npmjs.com/package/serverless-iam-roles-per-function)

Define IAM permission per function!

#### [serverless-latest-layer-version](https://www.npmjs.com/package/serverless-latest-layer-version)

Always get the latest version of AWS Lambda Layers 


#### [serverless-apigw-binary](https://www.npmjs.com/package/serverless-apigw-binary)

Allows you to enable binary files support in APIGW
