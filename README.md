What I learned

The purpose of this project was to practice the full job of a solutions architect: starting from a
client's business problem (cheap, scalable short links for a small agency with no IT team), choosing
the right AWS services, and explaining why each choice fits.

The biggest lesson came from troubleshooting. My website returned an S3 "Access Denied" error, and I
had to go back step by step to find the cause. The bucket policy JSON had the wrong ARN: I had used the
bucket's ARN in the `AWS:SourceArn` condition instead of the CloudFront distribution's ARN, and some
values still had example names instead of my real resource names. I learned that the `Resource` line
says *what* can be accessed, while `AWS:SourceArn` says *who* is allowed, and both must match the real
resources.

I also learned how to serve a website securely through CloudFront with a private S3 bucket, how to
connect API Gateway to Lambda functions, and how to build a CloudWatch dashboard and alarms that email
me when errors happen. I tested the alarm by causing an error on purpose to prove it works.

Next, I want to rebuild this project with Terraform (Infrastructure as Code), so it can be deployed
and deleted with one command, and add user login with Amazon Cognito.
