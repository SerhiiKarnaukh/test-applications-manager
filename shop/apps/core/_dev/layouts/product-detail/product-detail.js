import './product-detail.scss';


function init() {
    // Product detail
    $('.product-links-wap a').click(function(){
        var this_src = $(this).children('img').attr('src');
        $('#product-detail').attr('src',this_src);
        return false;
      });
      $('#btn-minus').click(function(){
        var val = $("#var-value").html();
        val = (val=='1')?val:val-1;
        $("#var-value").html(val);
        $("#product-quanity").val(val);
        return false;
      });
      $('#btn-plus').click(function(){
        var val = $("#var-value").html();
        val++;
        $("#var-value").html(val);
        $("#product-quanity").val(val);
        return false;
      });
      $('.btn-size').click(function(){
        var this_val = $(this).html();
        $("#product-size").val(this_val);
        $(".btn-size").removeClass('btn-secondary');
        $(".btn-size").addClass('btn-success');
        $(this).removeClass('btn-success');
        $(this).addClass('btn-secondary');
        return false;
      });
      $('#carousel-related-product').slick({
        infinite: true,
        arrows: false,
        slidesToShow: 4,
        slidesToScroll: 3,
        dots: true,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 3
                }
            }
        ]
    });
}

export default init;
