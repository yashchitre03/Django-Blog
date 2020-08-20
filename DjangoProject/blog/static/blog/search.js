const value = JSON.parse(document.getElementById('optionSelected').textContent);
if (value != null) {
  const ele = document.querySelector(`[value = ${value}]`);
  ele.setAttribute("selected", "");
}