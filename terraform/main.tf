# https://www.terraform.io/downloads.html

provider "aws" {
    region = "eu-west-1"
}

resource "aws_lambda_function" "LambdaFunction" {
    description = ""
    function_name = "queryGenerator"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/queryGenerator-ee85aae8-7472-4a39-92a7-a8c763ca3f5b"
    s3_object_version = "jDea9TChpxsaiV.h0BdwefPYIGlzBceA"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-iam-LambdaExecutionRole-1QWRABE198OU6"
    runtime = "python3.8"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:dependencies:5",
        "arn:aws:lambda:eu-west-1:544116674215:layer:Test-Query-Management:13"
    ]
}

resource "aws_lambda_function" "LambdaFunction2" {
    description = ""
    function_name = "unpackThread"
    handler = "index.handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/unpackThread-761dd12e-79f6-43fb-a905-d67e6a893f84"
    s3_object_version = "qXPYbRImwyVnIY.rBGDOAN7cwL2bRvwX"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-iam-LambdaExecutionRole-1QWRABE198OU6"
    runtime = "nodejs12.x"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction3" {
    description = ""
    function_name = "libraryTest"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/libraryTest-ccbcf0dd-0b56-4bb0-b687-d4f5ce87311b"
    s3_object_version = "S2b1cb4hwvHKsaTFV8SDjOnXvdvKhPfI"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-iam-LambdaExecutionRole-1QWRABE198OU6"
    runtime = "python3.8"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:dependencies:5",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:1"
    ]
}

resource "aws_lambda_function" "LambdaFunction4" {
    description = ""
    function_name = "createUpdateSeriesFunction"
    handler = "create_update_series.create_update_item"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/createUpdateSeriesFunction-7574910b-b7f6-42df-87d4-a359503f3482"
    s3_object_version = "Wt1OCjJekqKID0jSXdOfzLtAg3iotvFD"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction5" {
    description = ""
    environment {
        variables {
            ME_CANDIDATES_THRESHOLD = "70"
            ME_MATCHING_THRESHOLD = "90"
        }
    }
    function_name = "programmeMatchFunction-test-ds"
    handler = "programme_match_req.p_match_req"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/programmeMatchFunction-test-ds-c2fba9ba-114d-4276-b379-c8394c9da9fb"
    s3_object_version = "TaF.TwmyG7Y2JOYc3vPZDRqzrXa2FA3P"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:11",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction6" {
    description = ""
    environment {
        variables {
            region_name = "eu-west-1"
        }
    }
    function_name = "adf-prismacloud-AccountNameLambda-1J7HJSBWZ70GQ"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/adf-prismacloud-AccountNameLambda-1J7HJSBWZ70GQ-bf159d1f-3ecf-43e5-8b7b-38b0de80d7fc"
    s3_object_version = "CWqUcw2veGxYUsALjDE.zrT6KVRsX1uc"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-prismacloud-AccountNameLambdaRole-1KBDPV1U87HFQ"
    runtime = "python3.7"
    timeout = 300
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction7" {
    description = ""
    function_name = "adf-iam-ProviderCreator-J6WN1QPQTFKB"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/adf-iam-ProviderCreator-J6WN1QPQTFKB-ecddff39-7b55-4064-a2ad-7fe9151c95d6"
    s3_object_version = "hZuECv2picOo5OpGSO_X88wiKO6lK8Ju"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-iam-LambdaExecutionRole-1QWRABE198OU6"
    runtime = "python3.7"
    timeout = 30
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction8" {
    description = ""
    environment {
        variables {
            N_MAX_ITEMS = "10"
        }
    }
    function_name = "unpackBulkRequest"
    handler = "unpackBulkReq.execute"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/unpackBulkRequest-7bdd217c-96f2-41a4-9fac-ac3b6167493c"
    s3_object_version = "WV7FXMEk5BSEhDS7SGZc7a_trJbJtZ91"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction9" {
    description = ""
    environment {
        variables {
            ELASTIC_URL = "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com/prova_index/_search"
        }
    }
    function_name = "queryCluster"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/queryCluster-cde80182-0414-44c4-bfd7-fa98a4840860"
    s3_object_version = "wJ4Im9jvTC0s1PW8tg327HxTJG.xq3ab"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-iam-LambdaExecutionRole-1QWRABE198OU6"
    runtime = "python3.8"
    timeout = 10
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:dependencies:5",
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:1"
    ]
}

resource "aws_lambda_function" "LambdaFunction10" {
    description = ""
    function_name = "programmeMatchFunctionGet-test-ds"
    handler = "programme_match_req.p_match_req_get"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/programmeMatchFunctionGet-test-ds-8b886a35-0509-4fa3-9bf4-1748b38a284d"
    s3_object_version = "jEbC795blbKzk3M98gfH41fCEWQhyJsE"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:11",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction11" {
    description = ""
    environment {
        variables {
            ELASTIC_INDEX = "programme_index"
            ELASTIC_URL = "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com"
        }
    }
    function_name = "aliasManagement"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/aliasManagement-0412a670-d27b-4408-b11e-9addd7f900b8"
    s3_object_version = "6Tsz9Sdih2m3XaS89gF_qjDxQFH7yg.S"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-iam-LambdaExecutionRole-1QWRABE198OU6"
    runtime = "python3.8"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:dependencies:5",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:6",
        "arn:aws:lambda:eu-west-1:544116674215:layer:alias_management:2"
    ]
}

resource "aws_lambda_function" "LambdaFunction12" {
    description = ""
    function_name = "createUpdateFunction"
    handler = "create_update.create_update_item"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/createUpdateFunction-10785073-d6ac-488e-99a2-422490cd9e93"
    s3_object_version = "hdSkd33oZuwXXn9qhZsPeYhGuuclw0UC"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8",
        "arn:aws:lambda:eu-west-1:544116674215:layer:alias_management:2"
    ]
}

resource "aws_lambda_function" "LambdaFunction13" {
    description = "SAM unpackBulk"
    environment {
        variables {
            CHUNK_SIZE = "100"
        }
    }
    function_name = "unpackBulkThread-test"
    handler = "app.lambdaHandler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/unpackBulkThread-test-8d3a8898-4b88-4cf1-a61d-63c574f3e24e"
    s3_object_version = "7g85epWr6p4iRlBlD1JIfk9dzzgbnWEt"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "nodejs12.x"
    timeout = 30
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction14" {
    description = ""
    environment {
        variables {
            ME_CANDIDATES_THRESHOLD = "70"
            ME_MATCHING_THRESHOLD = "90"
        }
    }
    function_name = "programmeMatchFunction"
    handler = "programme_match_req.p_match_req"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/programmeMatchFunction-bef5404a-770a-4a8a-bd7d-ebfb96ef001c"
    s3_object_version = "8FHa3Uyu6eiyJ0iLwtL51V67Vh45yg0c"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:11",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction15" {
    description = "EC2 and RDS instance scheduler, version v3.0.0"
    environment {
        variables {
            Timezone = "Europe/Rome"
            DryRun = "False"
        }
    }
    function_name = "adf-instance-scheduler-InstanceSchedulerMain"
    handler = "scheduler.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/adf-instance-scheduler-InstanceSchedulerMain-6683ba91-9e2a-4101-a6e5-2de733889b5d"
    s3_object_version = "rGxoIKFhtCJ.nZEREx5.CwHIDfZ3ySq2"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-instance-scheduler-SchedulerRole-1E3M2VYSR0OA5"
    runtime = "python3.7"
    timeout = 300
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction16" {
    description = ""
    function_name = "programmeMatchFunctionGet"
    handler = "programme_match_req.p_match_req_get"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/programmeMatchFunctionGet-d98a15b3-fbe9-488a-9fbf-ae1e3d9fc9d4"
    s3_object_version = "1lmmhVY3E_u7WfAO7dYc4FZ6RfkvJzTD"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:11",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction17" {
    description = ""
    function_name = "createUpdateFunction-test-ds"
    handler = "create_update.create_update_item"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/createUpdateFunction-test-ds-e8ad02e3-d889-41eb-ad88-b5d0ed2826a1"
    s3_object_version = "xCZsxVpxh9ONFK4FjEda1SvWkLHhgCYT"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8",
        "arn:aws:lambda:eu-west-1:544116674215:layer:alias_management:2"
    ]
}

resource "aws_lambda_function" "LambdaFunction18" {
    description = ""
    function_name = "createAliasFunction"
    handler = "create_update.create_alias_item"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/createAliasFunction-5974a153-8729-444d-bfef-2a526baf6a63"
    s3_object_version = ".MElVHTAxOx7u_dydc.BdSXFa3.YKNZO"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8",
        "arn:aws:lambda:eu-west-1:544116674215:layer:alias_management:2"
    ]
}

resource "aws_lambda_function" "LambdaFunction19" {
    description = ""
    function_name = "manageResponse"
    handler = "manage_es_response.manage_response_api"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/manageResponse-c5924452-b59a-4a91-9465-d27c84dbdc5c"
    s3_object_version = "1tLuj1UNWAGjStzfNuKUYP5ytzfL2rSx"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:11",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction20" {
    description = ""
    function_name = "seriesMatchFunction"
    handler = "series_match_req.s_match_req"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/seriesMatchFunction-1eb4c126-fafe-427f-953a-8086ca56f5dd"
    s3_object_version = "yFCVezSIsgToj8mlqPIeXZi5H3qCm64Y"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:query_management:11",
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8"
    ]
}

resource "aws_lambda_function" "LambdaFunction21" {
    description = ""
    environment {
        variables {
            N_MAX_ITEMS = "10"
        }
    }
    function_name = "unpackBulkRequest-test-ds"
    handler = "unpackBulkReq.execute"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/unpackBulkRequest-test-ds-17788505-5b34-4b19-b14f-4648f26dbed4"
    s3_object_version = "QQ7bU8oYK4degfKmTRieExqrtKKI4kNa"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction22" {
    description = ""
    function_name = "createAliasFunction-test-ds"
    handler = "create_update.create_alias_item"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/createAliasFunction-test-ds-e330ecb9-0306-4672-a623-7a8193b32f81"
    s3_object_version = "eWQF3GtPAfay0Hag2hFJEQAufx5UAr23"
    memory_size = 256
    role = "arn:aws:iam::544116674215:role/matchingEngineIamLambdaExecutionRole"
    runtime = "python3.8"
    timeout = 63
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:eu-west-1:544116674215:layer:elasticsearch_metadata:8",
        "arn:aws:lambda:eu-west-1:544116674215:layer:alias_management:2"
    ]
}

resource "aws_lambda_function" "LambdaFunction23" {
    description = "Calls the GuardDuty Master lambda to invite itself to GuardDuty"
    function_name = "adf-guardduty-GuardDutyInviteFunction-39JGM8S6YUEN"
    handler = "member.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/adf-guardduty-GuardDutyInviteFunction-39JGM8S6YUEN-5c4083a6-f862-45f2-8d28-58c89ec6b374"
    s3_object_version = "qrUv_rDzpjjtUbXg_GUyW5g42oAVkmI9"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-guardduty-MemberLambdaExecutionRole-1NCIWEMK2Q414"
    runtime = "python3.7"
    timeout = 30
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction24" {
    description = ""
    environment {
        variables {
            region_name = "eu-west-1"
        }
    }
    function_name = "adf-prismacloud-PrismaOnboardLambda-1WLJYQW5HJQOO"
    handler = "lambda_function.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/adf-prismacloud-PrismaOnboardLambda-1WLJYQW5HJQOO-396551e7-d5e7-4342-9ae5-c0069f5a8e05"
    s3_object_version = "3SDAyfwzwKvo9J7BbRW52DnJjIBStiat"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-prismacloud-PrismaOnboardLambdaRole-FH7W560GDP2X"
    runtime = "python3.7"
    timeout = 600
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction25" {
    description = ""
    function_name = "adf-vpc-AuthorizationLambda-PJS3JU2KS3F7"
    handler = "r53auth.lambda_handler"
    s3_bucket = "awslambda-eu-west-1-tasks"
    s3_key = "/snapshots/544116674215/adf-vpc-AuthorizationLambda-PJS3JU2KS3F7-42fba188-a22a-4508-b039-9ae14d625bef"
    s3_object_version = "fgr8B4FYk7ntZo.m98zzDyWANkJWvoqG"
    memory_size = 128
    role = "arn:aws:iam::544116674215:role/adf-vpc-AuthorizationLambdaRole-1DH53LNQLWC5Q"
    runtime = "python3.7"
    timeout = 60
    tracing_config {
        mode = "PassThrough"
    }
}
