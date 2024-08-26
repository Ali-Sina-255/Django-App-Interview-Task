$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location == "/login";
          });
          if (response.status == "Failed") {
            swal(response.message, "", "error");
          }
          console.log("raise error message");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          // adding subtotal tex  grand_total

          ApplyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["total"],
            response.cart_amount["grand_total"]
          );
        }
      },
    });
  });
  // place the cart item quantity on load
  $(".item_qty").each(function () {
    var the_id = $(this).attr("id");
    var qty = $(this).attr("data-qty");
    console.log(qty);
    $("#" + the_id).html(qty);
  });

  // Decrease the card quantity
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    cart_id = $(this).attr("id");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location == "/login";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty-" + food_id).html(response.qty);
          if (window.location.pathname == "/cart/") {
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

  // place the cart item quantity on load
  // DELETE CART_ITEM
  $(".delete_cart").on("click", function (e) {
    e.preventDefault();
    cart_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        console.log(response);
        if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_counter"]);
          swal(response.status, response.message, "success");
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
  // DELETE CART ITEM WITHOUT RELOADING PAGE
  function removeCartItem(cartItemQty, cart_id) {
    if (cartItemQty <= 0) {
      document.getElementById("cart-item-" + cart_id).remove();
      console.log("this is not working in this time ");
    }
  }

  // CHECK IF CART EMPTY
  function CheckEmptyCart() {
    var cart_counter = document.getElementById("cart_counter").innerHTML;
    if (cart_counter == 0) {
      document.getElementById("empty_cart").style.display = "block";
    }
  }

  // Cart Amount
  function ApplyCartAmount(subtotal, total, grand_total) {
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);
      $("#total").html(total);
      $("#grand_total").html(grand_total);
    }
  }

  $(".add_hour").on("click", function (e) {
    e.preventDefault();
    var day = document.getElementById("id_day").value;
    var from_hour = document.getElementById("id_from_hour").value;
    var to_hour = document.getElementById("id_to_hour").value;
    var is_closed = document.getElementById("id_is_closed").checked;
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    var url = document.getElementById("add_hour_url").value;
    console.log(day, from_hour, to_hour, closed, csrf_token);
    if (is_closed) {
      is_closed = "True";
      condition = 'day != ""';
    } else {
      is_closed = "False";
      condition = 'day != "" && from_hour != "" && to_hour != ""';
    }
    if (eval(condition)) {
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
          if (response.status == "success") {
            if (response.is_closed == "Closed") {
              html =
                "<tr id='hour-'+response.id+'><td><b>" +
                response.day +
                "</b></td><td>Closed</td><td><a class='remove_hour' data-url='/accounts/vendor/opening_hours/remove/'+response.id+'/'>Remove</a></td></tr>";
            } else {
              html =
                "<tr id='hour-'+response.id+'><td><b>" +
                response.day +
                "</b></td><td>" +
                response.from_hour +
                " - " +
                response.to_hour +
                "</td><td><a class='remove_hour' data-url='/accounts/vendor/opening_hours/remove/'+response.id+'>Remove</a></td></tr>";
            }
            $(".opening_hours").append(html);
            document.getElementById("opening_hours").reset();
          } else {
            swal(response.message, "", "error");
          }
        },
      });
    } else {
      swal("Please fill the fill");
    }
  });

  $(document).on("click", ".remove_hour", function (e) {
    e.preventDefault();
    url = $(this).attr("data-url");
    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == "success") {
          document.getElementById("hour-" + response.id).remove();
        }
      },
    });
  });
});
