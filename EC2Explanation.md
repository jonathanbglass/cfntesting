Secure Web Server explanation
=====
## Requirements
* SSH accessible only from two IP addresses (A: 204.13.56.3), (B: 176.33.122.64)
* Two users: Alice & Bob
* Secure Web Site only other port open, exposed to the world
* Provide a cloudformation template to handle this

## Assumed Requirements
* Web Server can run Amazon Linux on a small (T2.micro) machine type
* Web Server can be in a Public subnet
* Need a VPC
* Need a security group for the web Server
 * Allow inbound 443 from 0.0.0.0/0
 * Allow inbound SSH from 2 IP addresses

## Solution Process
1. Create a basic CFN template that will spin up a VPC with Public and Private subnets & test
1a. Test command:
    aws cloudformation validate-template --template-body file://c:/users/dad/github/cfntesting/web_server_cloudformation.json
1b. find a sample CFN template and modify it to fit the need
2. Add an Amazon Linux AMI to that CFN template, t2.micro
3. Add a script to create the two users, Alice and Bob, during deployment
4. Configure the script to add a web Server & launch it on startup
5. Make sure Bob and Alice can make changes to the website directory
6. Assign my SSH key to the server at deployment
7. Upload a website to S3:  aws s3 cp website.zip s3://jonathanglass.cloud/files/
8. Have USERDATA scripts pull down sample website from my domain (https://jonathanglass.cloud/files/website.zip)
9. Extract those files to /var/www/html

## Conclusion
1. This took about 3 hours; I struggled a little with the CFN Template, as I'd grabbed an older sample and had to rewrite it
2. I apologize for the self-signed certificate. The connection is encrypted as required, but not ideal.
3. If I had more time, I'd add a CloudFront distribution and leverage CloudFront ssl certificates
4. I dislike storing the user credentials in the CFN template. I'd prefer to use a key management system, or a centralized authentication system. Unless the user already has their credentials created (ssh keys or a known password), creating random passwords, sharing them with the end users, and requiring them to change the passwords immediately is acceptable.
5. Ideally I'd reference each user's SSH public keys, add them to the user's ~/.ssh/authorized_keys file, and leave PasswordAuthentication disabled.
6. I acknowledge that this CFN template is brittle. It'll only work on US-EAST-2. Again, if this were for Production use, I'd add a Mapping of AMI-IDs and REGIONS and let the user pick a region.
7. If this were a static web site, I'd actually steer the customer toward using an S3 bucket as a website, front-ending that with CloudFront, and restricting access to the bucket to ONLY CloudFront. But that would also require training on the customer's part.
