import os
def start(hostname):
  with open(hostname+'pre', 'r') as file1:
    with open(hostname+'post', 'r') as file2:
      same = set(file1).difference(file2)
  same.discard('\n')

  with open(hostname+'post', 'r') as file1:
    with open(hostname+'pre', 'r') as file2:
      same1 = set(file1).difference(file2)
  same1.discard('\n')


  with open('diff_output_file.txt', 'w') as file_out:
    for line in same:
      file_out.write("########")
      file_out.write("\n")
      file_out.write(line)
    for line1 in same1:
      file_out.write(line1)
      file_out.write("########")
      file_out.write("\n")
  fileempty =  os.stat("diff_output_file.txt").st_size == 0
  print fileempty
  if fileempty:
    result = "ok"
  else:
    result = "different"
  return result


    
