document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("message");
  const placeholderText = "Type something...";
  let i = 0;

  function typePlaceholder() {
    if (i < placeholderText.length) {
      inputField.setAttribute("placeholder", placeholderText.substring(0, i + 1));
      i++;
      setTimeout(typePlaceholder, 200); // Adjust typing speed here
    }
  }

  typePlaceholder();
});
