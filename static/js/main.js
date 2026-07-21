//////////////////////////////////// product image in single product
const mainImage = document.getElementById('mainImage');
const zoomBox = document.getElementById('zoomBox');
const zoomLens = document.getElementById('zoomLens');
function isMobile() {
    return window.innerWidth <= 768;
}
if (mainImage) {
  
  mainImage.addEventListener('mousemove', function(event) {
      if (isMobile()) return;
      const { left, top, width, height } = mainImage.getBoundingClientRect();
      const x = event.clientX - left;
      const y = event.clientY - top;
      const lensSize = 80;
      const lensX = Math.max(0, Math.min(x - lensSize / 2, width - lensSize));
      const lensY = Math.max(0, Math.min(y - lensSize / 2, height - lensSize));
      zoomLens.style.left = `${lensX}px`;
      zoomLens.style.top = `${lensY}px`;
      const zoomLevel = 2;
      zoomBox.style.backgroundImage = `url(${mainImage.src})`;
      zoomBox.style.backgroundSize = `${width * zoomLevel}px ${height * zoomLevel}px`;
      zoomBox.style.backgroundPosition = `-${lensX * zoomLevel}px -${lensY * zoomLevel}px`;
      zoomLens.classList.remove('hidden');
      zoomBox.classList.remove('hidden');
  });
}
if (mainImage) {
  mainImage.addEventListener('mouseleave', function() {
      zoomLens.classList.add('hidden');
      zoomBox.classList.add('hidden');
  });
}
function changeImage(element) {
    mainImage.src = element.src;
}
//////////////////////////////// Quantity input
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".quantity-container").forEach(container => {
    const input = container.querySelector("input[type='number']");
    const incrementButton = container.querySelector("button[data-action='increment']");
    const decrementButton = container.querySelector("button[data-action='decrement']");

    incrementButton.addEventListener("click", function () {
      let value = parseInt(input.value, 10);
      input.value = value + 1;
    });

    decrementButton.addEventListener("click", function () {
      let value = parseInt(input.value, 10);
      if (value > 1) {
        input.value = value - 1;
      }
    });
  });
});
////////////////////////////////////////// modal login register
document.querySelectorAll(".open-modal").forEach((button) => {
  button.addEventListener("click", () => {
    const modalId = button.getAttribute("data-modal");
    const modal = document.getElementById(modalId);
    const modalBox = modal.querySelector(".modal-box");

    modal.classList.remove("hidden");
    setTimeout(() => {
      modal.classList.add("opacity-100");
      modalBox.classList.remove("opacity-0", "scale-90");
    }, 10);
  });
});
document.querySelectorAll(".close-modal").forEach((button) => {
  button.addEventListener("click", () => {
    const modal = button.closest(".modal");
    const modalBox = modal.querySelector(".modal-box");
    modal.classList.remove("opacity-100");
    modalBox.classList.add("opacity-0", "scale-90");
    setTimeout(() => modal.classList.add("hidden"), 300);
  });
});
document.querySelectorAll(".modal").forEach((modal) => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      const modalBox = modal.querySelector(".modal-box");
      modal.classList.remove("opacity-100");
      modalBox.classList.add("opacity-0", "scale-90");
      setTimeout(() => modal.classList.add("hidden"), 300);
    }
  });
});
///////////////////////////////////////// verify 6 code
const inputElements = [...document.querySelectorAll('input.code-input')]
if (inputElements) {
  // window.addEventListener("load", () => inputElements[0].focus());
  inputElements.forEach((ele,index)=>{
    ele.addEventListener('keydown',(e)=>{
      if(e.keyCode === 8 && e.target.value==='') inputElements[Math.max(0,index-1)].focus()
    })
    ele.addEventListener('input',(e)=>{
      const [first,...rest] = e.target.value
      e.target.value = first ?? ''
      const lastInputBox = index===inputElements.length-1
      const didInsertContent = first!==undefined
      if(didInsertContent && !lastInputBox) {
        inputElements[index+1].focus()
        inputElements[index+1].value = rest.join('')
        inputElements[index+1].dispatchEvent(new Event('input'))
      }
    })
  })
}
function onSubmit(e){
  e.preventDefault()
  const code = inputElements.map(({value})=>value).join('')
  console.log(code)
}


//////////////////////////////////////////// open and close mobile navbar
document.addEventListener("DOMContentLoaded", function () {
  const menu = document.getElementById("mobile-menu");
  const overlay = document.getElementById("overlay");
  const openBtn = document.querySelector(".menu-mobile");
  function openMenu() {
    menu.classList.remove("translate-x-full");
    overlay.classList.remove("hidden");
    overlay.classList.add("opacity-100");
  }
  function closeMenu() {
    menu.classList.add("translate-x-full");
    overlay.classList.add("hidden");
    overlay.classList.remove("opacity-100");
  }
  openBtn.addEventListener("click", openMenu);
  overlay.addEventListener("click", closeMenu);
});
//////////////////////////////////////////// open and close menu/submenu mobile
document.addEventListener("DOMContentLoaded", function () {
  const menuToggles = document.querySelectorAll(".menu-toggle");
  menuToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const submenu = this.nextElementSibling;
      const icon = this.querySelector("img");
      if (submenu.classList.contains("hidden")) {
        submenu.classList.remove("hidden");
        icon.classList.add("rotate-180");
      } else {
        submenu.classList.add("hidden");
        icon.classList.remove("rotate-180");
      }
    });
  });
});
/////////////////////////////////////////// progressBar
window.addEventListener("scroll", function () {
  let scrollTop = document.documentElement.scrollTop; // میزان اسکرول شده
  let scrollHeight =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight; // ارتفاع کل صفحه
  let scrollPercentage = (scrollTop / scrollHeight) * 100; // محاسبه درصد اسکرول
  document.getElementById("progressBar").style.width = scrollPercentage + "%"; // تغییر عرض نوار
});
//////////////////////////////// loading
window.addEventListener("load", function () {
  const loadingScreen = document.getElementById("loading");
  setTimeout(() => {
    loadingScreen.classList.add("opacity-0");
  }, 500);
  setTimeout(() => {
    loadingScreen.classList.add("hidden");
  }, 1000);
});
//////////////////////////////// btn go to top
document.getElementById("btn-back-to-top").addEventListener("click", function() {
  window.scrollTo({
      top: 0,
  });
});
/////////////////////////////// faq
function toggleFAQ(id) {
  const content = document.getElementById(`faq${id}`);
  const icon = content.previousElementSibling.querySelector('.icon');
  if (content.classList.contains('open')) {
      content.classList.remove('open');
      icon.textContent = '+';
  } else {
      content.classList.add('open');
      icon.textContent = '-';
  }
}
/////////////////////////////// rules
function toggleRules(id) {
  const content = document.getElementById(`rules${id}`);
  const icon = content.previousElementSibling.querySelector('.icon');
  if (content.classList.contains('open')) {
      content.classList.remove('open');
      icon.textContent = '+';
  } else {
      content.classList.add('open');
      icon.textContent = '-';
  }
}
/////////////////////////////// price filter
let priceFilter = document.querySelectorAll("#shop-price-slider"),
  priceMinFilter = document.querySelectorAll("#shop-price-slider-min"),
  priceMaxFilter = document.querySelectorAll("#shop-price-slider-max");
  priceFilter.forEach((e) => {
    noUiSlider.create(e, {
      cssPrefix: "range-slider-",
      start: [0, 1e8],
      direction: "rtl",
      margin: 1,
      connect: !0,
      range: { min: 0, max: 1e8 },
      format: {
        to: function (e) {
          return e.toLocaleString("en-US", {
            style: "decimal",
            maximumFractionDigits: 0,
          });
        },
        from: function (e) {
          return parseFloat(e.replace(/,/g, ""));
        },
      },
    }),
      e.noUiSlider.on("update", function (e, t) {
        t
          ? priceMaxFilter.forEach((a) => {
              a.innerHTML = e[t];
            })
          : priceMinFilter.forEach((a) => {
              a.innerHTML = e[t];
            });
      });
  })
/////////////////////////////// copy link page to clipboard
function copyToClipboard(event) {
  event.preventDefault();
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {}).catch(err => {});
}
//////////////////////////////////// open filter in search products
if (document.getElementById("mobile-filter")) {
  const filters = document.getElementById("mobile-filter");
  const openFilter = document.querySelector(".filter-mobile");
  const closeFilter = document.getElementById("closeFilter");
  function openMenu() {
    filters.classList.remove("translate-y-full");
  }
  function closeMenu() {
    filters.classList.add("translate-y-full");
  }
  openFilter.addEventListener("click", openMenu);
  closeFilter.addEventListener("click", closeMenu);
}