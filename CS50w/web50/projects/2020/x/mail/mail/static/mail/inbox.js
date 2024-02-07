document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#send").addEventListener("click", send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        // console.log(emails);
        // ... do something else with emails ...

        emails.forEach(email => {
          const element = document.createElement('div');
          element.innerHTML = `${email.sender} ${email.subject} ${email.timestamp}`;
          if (email.read == true){
            console.log("Read")
            element.className = 'email-container dark';
          } else {
            console.log("Unread")
            element.className = 'email-container';
          }
          element.addEventListener('click', () => view_mail(email.id));
          document.querySelector('#emails-view').appendChild(element);
        });
  });
}        

function view_mail(id){
  console.log("Trying to view email item")
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
      document.querySelector(".sender").innerHTML = email.sender
      document.querySelector(".recipients").innerHTML = email.recipients
      document.querySelector(".subject").innerHTML = email.subject
      document.querySelector(".timestamp").innerHTML = email.timestamp
      document.querySelector(".body").innerHTML = email.body
        // ... do something else with email ...
    });
}


function send_mail(event){
  event.preventDefault();
  // console.log("Send button clicked!");
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      
      if (result.message === "Email sent successfully.") {
        console.log(result.message);
        load_mailbox('sent');
      } else {
        console.log(`Email sending failed ${result.message}`);
      };
  })
  .catch(error => {
    console.error('Fetch error:', error.message);
  });
};