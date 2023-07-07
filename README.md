# redit
redit is a bash script designed for Unix environments to enhance your file editing experience by locally copying files from an ssh host before opening them in any desired editor.

This script allows you to efficiently work remote files on your preferred text editor as if they were on your local machine, eliminating the lag or latency issues typically associated with remote editing via ssh.

Upon completing your edits and exiting your editor, redit simplifies the upload process of the modified file back to the original remote host ensuring your changes are seamlessly synchronized.

## Requirements
- Unix environment (Linux, FreeBSD, macOS, Solaris, etc.)
- A text editor (Vi, Vim, Emacs, nano, etc) installed on your local machine

## Usage
To run the script, execute the following command in your terminal:

```
redit user@hostname:~/sourcepath/filename
```

Replace `user` with your username, `hostname` with the remote host's address, `sourcepath` with the path to the file on the remote host, and `filename` with the name of the file.

Alternatively, you can use the following command to reuse the last downloaded file:

```
redit last
```

When `last` is used as the argument, the script uses the last downloaded file in the temporary folder `.redit` that is created inside of the current working folder. 

This feature can be used multiple times and is particularly beneficial when you want to avoid the time it takes to download the same file again from the remote host, allowing you to make further changes to the same file locally and upload it to the remote host without the need for repetitive downloading. 

After exiting your editor the script will prompt you again to upload the edited file to the remote host and path from which the file was originally downloaded, eliminating the need to manually specify this values on any subsequent edit.

## License
This project is licensed under the GPLv3 License. 

