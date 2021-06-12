// Reference: https://bulma.io/documentation/elements/notification/#javascript-example
function init() {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    const $notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
}

export default {
  init
}
