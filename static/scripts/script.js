document.getElementById('conversion-form').addEventListener('submit', function(event) {
	event.preventDefault();

	const amount = parseFloat(document.getElementById('amount').value);
	const fromCurrency = document.getElementById('fromCurrency').value;
	const toCurrency = document.getElementById('toCurrency').value;

	fetch(`/convert?amount=${amount}&from_currency=${fromCurrency}&to_currency=${toCurrency}`)
		.then(response => response.json())
		.then(data => {
			if (data.error) {
				document.getElementById('result').textContent = data.error;
			} else {
				const formattedAmount = data.result.toLocaleString('en-US', {
					style: 'currency',
					currency: toCurrency,
					minimumFractionDigits: 4
				});
				document.getElementById('result').textContent = `${amount.toFixed(2)} ${fromCurrency} is equal to ${formattedAmount}`;
			}
		})
		.catch(error => {
			console.error('Error:', error);
			document.getElementById('result').textContent = 'An error occurred. Please try again later.';
		});
});


window.addEventListener('scroll', function() {
	const headers = document.querySelectorAll('.sub-header');

	headers.forEach(function(header) {
		if (window.scrollY > 0) {
			header.classList.add('scrolled');
		} else {
			header.classList.remove('scrolled');
		}
	});
});


document.getElementById('contact-link').addEventListener('click', function(event) {
	event.preventDefault();

	const targetSection = document.getElementById('contact-us-id');
	if (targetSection) {
		targetSection.scrollIntoView({
			behavior: 'smooth'
		});
	}

	document.querySelector('.active').classList.remove('active');
	this.classList.add('active');
});


document.getElementById('home-link').addEventListener('click', function(event) {
	event.preventDefault();
	window.scrollTo({
		top: 0,
		behavior: 'smooth'
	});

	document.querySelector('.active').classList.remove('active');
	this.classList.add('active');
});
