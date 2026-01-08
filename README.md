# TrueNAS Cert Uploader

A simple python script to replace an existing SSL cert on a [TrueNAS](https://www.truenas.com) server with a new one and loading the new one as the UI Cert. It also deletes the one replaced.

## Usage

Duplicate the `config.example.json` file and name it `config.json`.  Replace the values in it with the ones valid to your server.  The script names the cert by concatenating the epoch time to the `cert_name_prefix` value.  It also uses the prefix to determine what certs to delete. (So don't use that prefix for other unrelated certs you might have loaded on the server.)

## Background
I had a wildcard certificate being acquired via [Cert Warden](https://www.certwarden.com). Once acquired, scripts can be run to move the certs to the locations needed.  This turned out to be the cleanest way I could get the cert properly loaded into TrueNAS in an automated fashion.  The script makes use of the official [TrueNAS WebSocket Client](https://github.com/truenas/api_client).  In order for the script to run, you need to install the client library:
```bash
pip install git+https://github.com/truenas/api_client.git
```

## Feedback
I make no promises that this will work for you.  I don't even claim it won't break your setup. I make no claims to having written stellar Python.  Please feel free to make suggestions or pull requests. They are welcomed!

