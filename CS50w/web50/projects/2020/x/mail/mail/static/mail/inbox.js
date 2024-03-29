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
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#mail-buttons').style.display = 'none';
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
  document.querySelector('#mail-buttons').style.display = 'none';
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
          element.innerHTML = `
            <div class="email-sender-subject">
              <span class="email-sender"><strong>${email.sender} - </strong></span>
              <span class="email-subject">${email.subject}</span>
            </div>
            <div class="email-timestamp">${email.timestamp}</div>
          `;
          if (email.read == true){
            // console.log("Read")
            element.className = 'email-container form-control dark';
          } else {
            // console.log("Unread")
            element.className = 'email-container form-control';
          }
          element.addEventListener('click', () => view_mail(email.id));
          document.querySelector('#emails-view').appendChild(element);
        });
  });
}        

function view_mail(id){
  // console.log("Trying to view email item")
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  const user = document.querySelector("h2").innerHTML
  document.querySelector('#mail-buttons').style.display = 'block';
  
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      // console.log(email);
      // ... do something else with email ...
      document.querySelector(".sender").innerHTML = `<strong>From: </strong>${email.sender}`
      document.querySelector(".recipients").innerHTML = `<strong>To: </strong>${email.recipients}`
      document.querySelector(".subject").innerHTML = `<strong>Subject: </strong>${email.subject}`
      document.querySelector(".timestamp").innerHTML = `<strong>Date Sent: </strong>${email.timestamp}`
      document.querySelector(".body").innerHTML = email.body

	  const sender = email.sender;
		if (user === sender){
      document.querySelector('#mail-buttons').style.display = 'none';
    } else if (email.archived){
      document.querySelector(".archive-button").innerHTML = "Unarchive"
      document.querySelector(".archive-button").id = "unarchive"
      document.querySelector(".archive-button").addEventListener("click", () => unarchive_mail(id))
      document.querySelector(".reply-button").addEventListener("click", () => reply_email(id))
    } else {
      document.querySelector(".archive-button").innerHTML = "Archive"
      document.querySelector(".archive-button").id = "archive"
      document.querySelector(".archive-button").addEventListener("click", () => archive_mail(id))
      document.querySelector(".reply-button").addEventListener("click", () => reply_email(id))
    }


  });

function reply_email(id){
  // console.log(id)
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#mail-buttons').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#compose-recipients').value = email.sender
    // console.log(email.subject.slice(0,3))
    if (email.subject.slice(0,3) === "Re:"){
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n ${email.body}`;
    document.querySelector('#compose-body').focus();
    document.querySelector('#compose-body').setSelectionRange(0, 0);
  })
};


  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  
}

function archive_mail(id){
  // console.log(`Trying to archive mail ${id}`)
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(result => {
    // Print result
    console.log(result);
    load_mailbox('inbox')
  })
}

function unarchive_mail(id){
  // console.log(`Trying to unarchive mail ${id}`)
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('inbox')
  })
  
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
        // console.log(result.message);
        load_mailbox('sent');
      };
  })
  .catch(error => {
    console.error('Fetch error:', error.message);
  });
};