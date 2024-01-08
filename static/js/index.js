AOS.init({
  duration: 1500,
})

// For card slider 
$('.owl-carousel').owlCarousel({
  loop: false,
  margin: 10,
  nav: true,
  responsive: {
    0: {
      items: 1
    },
    476: {
      items: 2
    },
    768: {
      items: 3
    },
    992: {
      items: 4
    },
    1200: {
      items: 5
    }
  }
})

// For scroll to top btn

const topbtn = document.getElementById('scrollToTopBtn');

const displayButton = () => {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
      topbtn.classList.add('show'); // Add the "show" class when scrolling down
    } else {
      topbtn.classList.remove('show'); // Remove the "show" class when at the top
    }
  });
};

const scrollToTop = () => {
  topbtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth'
    });
  });
};

displayButton();
scrollToTop();

// For quantity selector

$(document).ready(function () {
  $(".plus-btn").click(function () {
    var quantityInput = $(this).siblings(".quantity-selector-input");
    var currentValue = parseInt(quantityInput.val());
    if (currentValue < 6) { // Check the max value
      quantityInput.val(currentValue + 1);
    }
  });

  $(".minus-btn").click(function () {
    var quantityInput = $(this).siblings(".quantity-selector-input");
    var currentValue = parseInt(quantityInput.val());
    if (currentValue > 1) { // Check the min value
      quantityInput.val(currentValue - 1);
    }
  });

  $(".quantity-selector-input").on("input", function () {
    var currentValue = parseInt($(this).val());
    if (isNaN(currentValue) || currentValue < 1) {
      $(this).val(1);
    } else if (currentValue > 6) {
      $(this).val(6);
    }
  });
});

// For auto hide alert

document.addEventListener('DOMContentLoaded', function() {
  // Find all alert elements with the warning class
  const warningAlerts = document.querySelectorAll('.alert-warning');

  // Loop through each warning alert and hide it after a specified time
  warningAlerts.forEach(alert => {
    const timeout = 4000; // Adjust the duration in milliseconds
    setTimeout(() => {
      alert.style.display = 'none';
    }, timeout);
  });
});

// For signup box
let timeoutId;
let loginLink = document.getElementById('login-link');
let signupBox = document.querySelector('.signup-box');

// Check if the login link is present and the screen width is greater than 992 pixels
if (loginLink && window.innerWidth > 992) {
  loginLink.addEventListener('mouseenter', function () {
    clearTimeout(timeoutId);
    showSignupBox();
  });

  loginLink.addEventListener('mouseleave', function () {
    timeoutId = setTimeout(hideSignupBox, 400);
  });

  signupBox.addEventListener('mouseenter', function () {
    clearTimeout(timeoutId);
  });

  signupBox.addEventListener('mouseleave', function () {
    timeoutId = setTimeout(hideSignupBox, 400);
  });
}

function showSignupBox() {
  let a = setTimeout(() => {
    signupBox.style.display = 'block';
  }, 400);
}

function hideSignupBox() {
  signupBox.style.display = 'none';
}



// For user dropdown

$(document).ready(function () {
  var userDropdown = $('#dropdown');
  var userIcon = $('#user-icon');

  // Toggle dropdown on user icon click
  userIcon.click(function (e) {
    e.preventDefault();
    userDropdown.toggle();
  });

  // Hide dropdown when clicking outside of it
  $(document).click(function (e) {
    if (!userDropdown.is(e.target) && !userIcon.is(e.target)) {
      userDropdown.hide();
    }
  });

  // Hide dropdown when scrolling
  $(window).scroll(function () {
    userDropdown.hide();
  });
});


// For preventing any other input in phone number input box except numbers 

$(document).ready(function () {
  // Listen for input events on the phone number input field
  $('.phoneNumberInput').on('input', function () {
    // Remove any non-numeric characters
    var sanitizedInput = $(this).val().replace(/[^0-9]/g, '');
    $(this).val(sanitizedInput);
  });
});


// For the counter section

// Function to animate the counters
// Initialize the Intersection Observer
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const target = entry.target;
      const count = +target.getAttribute("data-target");
      const duration = 2000; // Adjust the duration as needed
      const increment = count / (duration / 10);
      let currentCount = 0;

      const updateCounter = () => {
        currentCount += increment;
        if (currentCount < count) {
          target.textContent = Math.floor(currentCount);
          requestAnimationFrame(updateCounter);
        } else {
          target.textContent = count;
        }
      };

      requestAnimationFrame(updateCounter);

      // Unobserve the target to stop updating once it's reached
      observer.unobserve(target);
    }
  });
});

// Observe all elements with the class "counter-item"
const counters = document.querySelectorAll(".counter-item");
counters.forEach(counter => {
  observer.observe(counter);
});


// Navbar close when touching outside or scrolling

$(document).ready(function () {
  // Close the navbar when clicking outside of it
  $(document).on('click', function (event) {
    var target = $(event.target);
    if (!target.closest('.navbar').length && $('.navbar-collapse').hasClass('show')) {
      $('.navbar-toggler').click();
    }
  });

  // Close the navbar when scrolling
  $(window).on('scroll', function () {
    if ($('.navbar-collapse').hasClass('show')) {
      $('.navbar-toggler').click();
    }
  });
});
