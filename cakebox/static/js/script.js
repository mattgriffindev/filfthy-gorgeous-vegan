/*----------------------------------------------------send-mail-*/

function sendMail(contactForm) {
	emailjs.send("service_l0dqag3", "template_30ofgfw", {
			"from_name": contactForm.name.value,
			"from_email": contactForm.email.value,
            "from_phone": contactForm.phone.value,
			"message": contact-form.messagebox.value
		})
		.then(
			function (response) {
				console.log("SUCCESS", response);
				alert("Your message has been sent");
				document.getElementById("contactForm").reset();
			},
			function (error) {
				console.log("FAILED", error);
			}
		);
	return false;
}