# Issue RSA private key + public key pair

```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```
