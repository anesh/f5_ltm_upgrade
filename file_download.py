import os
import requests

def download(host, creds, fp,ftype):
    chunk_size = 512 * 1024

    headers = {
        'Content-Type': 'application/octet-stream'
    }
    filename = os.path.basename(fp)
    if ftype == "ucs":
      uri = 'https://%s/mgmt/shared/file-transfer/ucs-downloads/%s' % (host, filename)
    else:
      uri = 'https://%s/mgmt/cm/autodeploy/qkview-downloads/%s' % (host, filename)
    requests.packages.urllib3.disable_warnings()
    

    with open(fp, 'wb') as f:
        start = 0
        end = chunk_size - 1
        size = 0
        current_bytes = 0

        while True:
            content_range = "%s-%s/%s" % (start, end, size)
            headers['Content-Range'] = content_range

            #print headers
            resp = requests.get(uri,
                                auth=creds,
                                headers=headers,
                                verify=False,
                                stream=True)

            if resp.status_code == 200:
                # If the size is zero, then this is the first time through the
                # loop and we don't want to write data because we haven't yet
                # figured out the total size of the file.
                if size > 0:
                    current_bytes += chunk_size
                    for chunk in resp.iter_content(chunk_size):
                        f.write(chunk)

                # Once we've downloaded the entire file, we can break out of
                # the loop
                if end == size:
                    break

            crange = resp.headers['Content-Range']

            # Determine the total number of bytes to read
            if size == 0:
                size = int(crange.split('/')[-1]) - 1

                # If the file is smaller than the chunk size, BIG-IP will
                # return an HTTP 400. So adjust the chunk_size down to the
                # total file size...
                if chunk_size > size:
                    end = size

                # ...and pass on the rest of the code
                continue

            start += chunk_size

            if (current_bytes + chunk_size) > size:
                end = size
            else:
                end = start + chunk_size - 1


