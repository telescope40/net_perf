In order to allow for anonymous upload and download to s3 buckets 
I need to create a series of s3 Buckets 
Allow the permission for the existing files to be public shared 
change the write access for files to be owned by the writer not the bucket owner 
permission to allow for anonymous upload was tricky I needed to create s3 policy to allow this 

CURL to download 
curl https://mrbucket-us-east-1.s3.amazonaws.com/news3object.txt --output news3object2.txt

Curl to Upload 

curl -X PUT -T  news3object.txt \
"https://mrbucket-ap-southeast-1.s3.amazonaws.com/news3object.txt"




```
{
    "Version": "2012-10-17",
    "Id": "scp-to-s3",
    "Statement": [
        {
            "Sid": "scp-to-s3",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::<bucketname>/*"
        }
    ]
}
```
