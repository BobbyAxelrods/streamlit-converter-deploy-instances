# Streamlit App Deployment on AWS EC2

This guide provides step-by-step instructions for deploying a Streamlit app on an AWS EC2 instance using the `tmux` session manager to keep the app running even after closing the SSH session.

## Prerequisites

- AWS account
- Basic knowledge of AWS EC2 and SSH

## Steps

1. **Create an EC2 instance**

   - Launch an EC2 instance on AWS with the desired specifications.
   - Adjust the security group to allow SSH traffic from anywhere or your specific IP address.

   ![EC2 Instance Creation](https://miro.medium.com/v2/resize:fit:828/format:webp/1*HNbVQld4NlJwcmmBwh7DTA.png)

2. **Adjust security group**

   - Configure the security group for your EC2 instance to allow SSH traffic.
   - Add a Custom TCP rule that allows Port Range 8501 with Source `0.0.0.0/0`.

   ![Security Group Configuration](https://miro.medium.com/v2/resize:fit:828/format:webp/1*60-27qb20YVjPg0rR0f-Lg.png)

3. **Save key pair in PEM format using SSH**

   - During the EC2 instance creation process, create a key pair.
   - Download and save the key pair (`key_pair.pem`) in a secure location. You will need it to connect to the EC2 instance.

4. **Connect to the EC2 instance**

   - Create a folder named "AWS" on your local machine and place the key pair (`key_pair.pem`) and the Streamlit app files in this folder.
   - Open a terminal and navigate to the folder you just created using the `cd` command.

     ```bash
     cd /path/to/AWS/
     ```

   - Connect to the EC2 instance using SSH with the following command:

     ```bash
     ssh -i "key_pair.pem" ubuntu@<Your Public DNS(IPv4) Address>
     ```

5. **Install required libraries from the `requirements.txt` file**

   - Inside the EC2 instance terminal, navigate to the directory where your Streamlit app is located.
   
     ```bash
     cd /home/ubuntu/streamlit/
     ```

   - Install the required libraries using the `requirements.txt` file.
   
     ```bash
     pip install -r requirements.txt
     ```

6. **Copy files from localhost to the AWS instance**

   - In your local machine's terminal, use the `scp` command to copy your Streamlit app files to the AWS instance.

     ```bash
     scp -i "key_pair.pem" -r /path/to/streamlit-app/ ubuntu@<Your Public DNS(IPv4) Address>:/home/ubuntu/streamlit/
     ```

7. **Configure inbound rules for the EC2 instance**

   - Go to the AWS Console, select your EC2 instance, and scroll down to the Security Groups section.
   - Click on Inbound Rules and edit the rules.
   - Add a Custom TCP rule that allows Port Range 8501 with Source `0.0.0.0/0`.

8. **Run the Streamlit app in a `tmux` session**

   - Install `tmux` on the EC2 instance if it's not already installed.

     ```bash
     sudo apt update
     sudo apt install tmux
     ```

   - Start a new `tmux` session:

     ```bash
     tmux new -s StreamSession
     ```

   - Inside the `tmux` session, navigate to the directory where your Streamlit app is located.

     ```bash
     cd /home/ubuntu/streamlit/
     ```

   - Activate your virtual environment if required.

   - Run your Streamlit app using the `streamlit run` command:

     ```bash
     streamlit run streamlit.py
     ```

     Replace `streamlit.py` with the actual file name of your Streamlit app.

   - Detach from the `tmux` session by pressing `Ctrl + B`, followed by `D`.

9. **Accessing the Streamlit app**

   - Close the SSH connection.
   - Open a web browser and enter the public IP address or DNS of your EC2 instance, followed by the Streamlit app port (usually 8501), in the address bar.
   
     ```
     http://<Your Public IP or DNS>:8501
     ```

   - You should now be able to access and interact with your deployed Streamlit app.

10. **Stopping the EC2 instance**

    - When you are finished using the Streamlit app, remember to stop the EC2 instance to avoid unnecessary costs.

## License

This project is licensed under the [MIT License](LICENSE).

