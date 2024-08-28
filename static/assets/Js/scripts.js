$(document).ready(function () {
  // Handle adding to cart
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    let food_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status === "login_required") {
          swal({
            title: response.message,
            icon: "info"
          }).then(function () {
            window.location.href = "/login";
          });
        } else if (response.status === "Failed") {
          swal({
            title: response.message,
            icon: "error"
          });
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          ApplyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["total"],
            response.cart_amount["grand_total"]
          );
        }
      },
    });
  });

  // Initialize cart item quantity on page load
  $(".item_qty").each(function () {
    let the_id = $(this).attr("id");
    let qty = $(this).attr("data-qty");
    console.log(qty);
    $("#" + the_id).html(qty);
  });

  // Handle decreasing cart quantity
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    let food_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");
    let cart_id = $(this).attr("id");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status === "login_required") {
          swal({
            title: response.message,
            icon: "info"
          }).then(function () {
            window.location.href = "/login";
          });
        } else if (response.status === "Failed") {
          swal({
            title: response.message,
            icon: "error"
          });
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          if (window.location.pathname === "/cart/") {
            removeCartItem(response.qty, cart_id);
            CheckEmptyCart();
          }
          ApplyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["total"],
            response.cart_amount["grand_total"]
          );
        }
      },
    });
  });

  // Handle deleting cart item
  $(".delete_cart").on("click", function (e) {
    e.preventDefault();
    let cart_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status === "Failed") {
          swal({
            title: response.message,
            icon: "error"
          });
        } else {
          $("#cart_counter").html(response.cart_counter["cart_counter"]);
          swal({
            title: response.status,
            text: response.message,
            icon: "success"
          });
          removeCartItem(0, cart_id);
          CheckEmptyCart();
        }
        ApplyCartAmount(
          response.cart_amount["subtotal"],
          response.cart_amount["total"],
          response.cart_amount["grand_total"]
        );
      },
    });
  });

  // Remove cart item
  function removeCartItem(cartItemQty, cart_id) {
    if (cartItemQty <= 0) {
      document.getElementById("cart-item-" + cart_id).remove();
      console.log("Cart item removed.");
    }
  }

  // Check if cart is empty
  function CheckEmptyCart() {
    let cart_counter = document.getElementById("cart_counter").innerHTML;
    if (cart_counter == 0) {
      document.getElementById("empty_cart").style.display = "block";
    }
  }

  // Apply cart amount to the page
  function ApplyCartAmount(subtotal, total, grand_total) {
    if (window.location.pathname === "/cart/") {
      $("#subtotal").html(subtotal);
      $("#total").html(total);
      $("#grand_total").html(grand_total);
    }
  }

  // Handle adding hours
  $(".add_hour").on("click", function (e) {
    e.preventDefault();
    let day = document.getElementById("id_day").value;
    let from_hour = document.getElementById("id_from_hour").value;
    let to_hour = document.getElementById("id_to_hour").value;
    let is_closed = document.getElementById("id_is_closed").checked;
    let csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    let url = document.getElementById("add_hour_url").value;
    console.log(day, from_hour, to_hour, is_closed, csrf_token);

    if (day && (!is_closed && from_hour && to_hour || is_closed)) {
      $.ajax({
        type: "POST",
        url: url,
        data: {
          day: day,
          from_hour: from_hour,
          to_hour: to_hour,
          is_closed: is_closed,
          csrfmiddlewaretoken: csrf_token,
        },
        success: function (response) {
          if (response.status === "success") {
            let html;
            if (response.is_closed === "Closed") {
              html = `<tr id='hour-${response.id}'><td><b>${response.day}</b></td><td>Closed</td><td><a class='remove_hour' data-url='/accounts/vendor/opening_hours/remove/${response.id}/'>Remove</a></td></tr>`;
              $(".opening_hours").append(html);
              document.getElementById("opening_hours").reset();
            } else {
              html = `<tr id='hour-${response.id}'><td><b>${response.day}</b></td><td>${response.from_hour} - ${response.to_hour}</td><td><a class='remove_hour' data-url='/accounts/vendor/opening_hours/remove/${response.id}'>Remove</a></td></tr>`;
              $(".opening_hours").append(html);
              document.getElementById("opening_hours").reset();
            }
            $(".opening_hours").append(html);
            document.getElementById("opening_hours").reset();
          } else {
            swal({
              title: response.message,
              icon: "error"
            });
          }
        },
      });
    } else {
      swal({
        title: "Please fill all fields",
        icon: "warning"
      });
    }
  });

  // Handle removing hours
  $(document).on("click", ".remove_hour", function (e) {
    e.preventDefault();
    let url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status === "success") {
          document.getElementById("hour-" + response.id).remove();
        }
      },
    });
  });
});
