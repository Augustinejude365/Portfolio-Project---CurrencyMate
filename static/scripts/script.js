// Block to handle the form submission for the currency conversion,
//  fetching data from the backend and updating the UI with the result or error message
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



// Block to implement header scroll effect
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

// Blocks to implement nav links scroll effect
// CONVERTER
document.getElementById('converter-link').addEventListener('click', function(event) {
	event.preventDefault();
	window.scrollTo({
		top: 0,
		behavior: 'smooth'
	});

	document.querySelector('.active').classList.remove('active');
	this.classList.add('active');
});

// CONTACT US
document.getElementById('contact-link').addEventListener('click', function(event) {
	event.preventDefault();

	const targetSection = document.getElementById('contact-us');
	if (targetSection) {
		targetSection.scrollIntoView({
			behavior: 'smooth'
		});
	}

	document.querySelector('.active').classList.remove('active');
	this.classList.add('active');
});

// ABOUT US
document.getElementById('about-link').addEventListener('click', function(event) {
	event.preventDefault();

	const targetSection = document.getElementById('about-us');
	if (targetSection) {
		targetSection.scrollIntoView({
			behavior: 'smooth'
		});
	}

	document.querySelector('.active').classList.remove('active');
	this.classList.add('active');
});




// Block to dynamically change the style of the nav links when section is visible
const sections = document.querySelectorAll('.converter-container, .about-wrapper, .contact-wrapper');

let currentActiveSection = null;

window.addEventListener('scroll', function() {
	const scrollY = window.scrollY;

	sections.forEach(section => {
		const sectionTop = section.offsetTop;
		const sectionHeight = section.offsetHeight;
		const isVisible = scrollY >= sectionTop && scrollY < sectionTop + sectionHeight;

		if (isVisible) {
			currentActiveSection = section;
			return; // Exit the loop once a visible section is found
		}
	});

	if (currentActiveSection) {
		const previouslyActiveLink = document.querySelector('.active');
		if (previouslyActiveLink) {
			previouslyActiveLink.classList.remove('active');
		}

		const currentSectionId = currentActiveSection.id;
		const listItemForActiveSection = document.querySelector(`nav.tabs ul li a[href="#${currentSectionId}"]`);

		if (listItemForActiveSection) {
			listItemForActiveSection.parentElement.classList.add('active');
		}
	}
});
