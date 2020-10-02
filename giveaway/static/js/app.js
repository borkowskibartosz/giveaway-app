// https://stackoverflow.com/questions/298772/django-template-variables-and-javascript

$(document).ready(function(){
  function getCookie(c_name) {
      if(document.cookie.length > 0) {
          c_start = document.cookie.indexOf(c_name + "=");
          if(c_start != -1) {
              c_start = c_start + c_name.length + 1;
              c_end = document.cookie.indexOf(";", c_start);
              if(c_end == -1) c_end = document.cookie.length;
              return unescape(document.cookie.substring(c_start,c_end));
          }
      }
      return "";
  }

  $(function () {
      $.ajaxSetup({
          headers: {
              "X-CSRFToken": getCookie("csrftoken")
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  /**
   * HomePage - Help section
   */
  var institutionCats
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      // console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // Filter by categories

      if (this.currentStep == 3) {

        var cList = [];
        $("input:checkbox[name='categories']").each(function () {
          if (this.checked) {
            cList.push(this.value); // Lista wybranych kategorii
          }
        });
        // console.log (cList);

        $("div[data-categories]").each(function () {
          institutionCats = $(this).data('categories').split(",")
          // console.log(institutionCats);
          let allFounded = cList.every(ai => institutionCats.includes(ai));
          if (!allFounded) {
            $(this).hide();
          } else {
            $(this).show();
          }
        })
      }
      // TODO: Validation



      //       var sThisVal = (this.checked);
      //       sList += (sList=="" ? sThisVal : "," + sThisVal);
      //   });
      //   console.log (sList);
      // }
      // }
      // var sList = "";
      // // $(this).attr('data-fullText')
      // // $( "body" ).data( "foo", 52 )
      // $('div[data=]').each(function () {
      //   sList += $(this).data('categories');
      // })
      // console.log (sList);



      // $('div.form-group--checkbox').each(function(i, obj) {
      //   if ($(this.id)
      // });




      //  function toggleFields() {
      //   var arr = ['3','4','5'];
      //   var value = $("#chosenmove1").val();

      //   if (jQuery.inArray(value, arr) > -1)
      //       $("#hideme").show();
      //   else
      //       $("#hideme").hide();

      //   }

      //   if (this.currentStep == 3) {
      //       // alert("TEST")
      //       //   var element = document.getElementById("aaa");
      //       //   element.parentNode.removeChild(element);
      //  }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
      if (this.currentStep == 5) {
        var bags = $('input[name=bags]').val()
        var orgName = $('input[name=organization]:checked').next().next().children(":first").text();
        if (bags == 1) {
          var bags_text = '1. worek darów'
        } else if (bags < 5) {
          var bags_text = bags + ' worki'
        } else {
          var bags_text = bags + ' worków'
        }
        $('span.icon-bag').next().text(bags_text)
        $('span.icon-hand').next().text('Dary otrzyma ' + orgName)
        var firstAddress = $('h4:contains("Adres odbioru:")').next().children(":first")
        var secondAddress = firstAddress.next();
        var postCode = secondAddress.next();
        var phoneNumber = postCode.next();
        var firstDate = $('h4:contains("Termin odbioru:")').next().children(":first")
        var secondDate = firstDate.next()
        var comments = secondDate.next()

        // console.log(firstDate)
        // console.log(secondDate)

        firstAddress.text($("input[name=address]").val());
        secondAddress.text($("input[name=city]").val());
        postCode.text($("input[name=postcode]").val());
        phoneNumber.text($("input[name=phone]").val());

        firstDate.text($("input[name=data]").val());
        secondDate.text($("input[name=time]").val());
        comments.text($("textarea[name=more_info]").val());

      }
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */


    submit(e) {
      e.preventDefault();

      $.ajax({
        data: {
            quantity: $('input[name=bags]').val(),
            categories: JSON.stringify(institutionCats),
            organization: $('input[name=organization]:checked').parent().parent().attr("id"),
            address: $("input[name=address]").val(),
            city: $("input[name=city]").val(),
            postcode: $("input[name=postcode]").val(),
            phone: $("input[name=phone]").val(),
            data: $("input[name=data]").val(),
            time: $("input[name=time]").val(),
            more_info: $("textarea[name=more_info]").val(),
        }, // get the form data
        type: 'POST', // GET or POST
        url: "#",
        // on success
        success: function() {
            // alert("Thank you. Form sent successfully ");
            location.href = "/confirmation"
        },
        // on error
        error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); 
        }
      });

      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
