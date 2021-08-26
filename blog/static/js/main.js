$(document).ready(function() {
    const csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });


    // search
    $('.header__form [type=submit]').click(function(e) {
        console.log('click');
        const form = $(this).closest('form');
        const input = form.find('input[type="text"]');
        const searchPhrase = input.val();
        if (!searchPhrase.trim().length) {
            e.preventDefault();
            input.toggleClass('active');
            if (input.hasClass('active')) {
                setTimeout(() => {
                    input.focus();
                }, 150);
            }

        }
    });

    const mobileMenu = $('.header__menu_mobile');
    $('.mobile-menu button').click(function() {
        mobileMenu.toggleClass('active');
        $(this).toggleClass('active');
    });

    // cats menu
    $('.cats-aside-group').click(function() {
        $(this).toggleClass('active');
    });

    $('.cats-aside-group .active').click(function(e) {
        e.preventDefault();
    });

    // term-arrow
    const termsGroup = $('.terms-group');
    let index = 0;
    let maxSlides = getMaxSlides();
    $('.term-arrow.next').click(function() {
        if (index < maxSlides) {
            index++;
            scrollTerms();
        }
    });

    $('.term-arrow.prev').click(function() {
        if (index > 0) {
            index--;
            scrollTerms();
        }
    });

    function scrollTerms(duration=200) {
        let width = termsGroup.find('.term-item:nth-child(2)').outerWidth(true);
        termsGroup.stop().animate({
            scrollLeft: Number(index) * width
        }, duration);

    }

    function getMaxSlides() {
        let visibleSlides = Math.floor($('.container').width() / termsGroup.find('.term-item:nth-child(2)').outerWidth());
        let allSlides = termsGroup.find('.term-item').length;
        return allSlides - visibleSlides;
    }

    function resetSlides() {
        maxSlides = getMaxSlides();
        index = 0;
        scrollTerms(0);
    }

    $(window).resize(function() {
        resetSlides();
    });

    // comments
    const formComment = $('.form-comment');
    if (localStorage.getItem('name') && localStorage.getItem('surname')) {
        formComment.find('[name="name"]').val(localStorage.getItem('name'));
        formComment.find('[name="surname"]').val(localStorage.getItem('surname'));
    }

    $('.comments-group').on('click', '.comment__cite', function(e) {
        e.preventDefault();
        const id = $(this).attr('href');
        const target = $(id);
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 150
            }, 500);
        }
    });

    $('.comments-group').on('click', '.comment__reply', function(e) {
        e.preventDefault();
    });

    $('.delete-replied-comment').click(function() {
        $parent = $(this).closest('.replied-message');
        $parent.slideUp(200);
        formComment.find('[name="reply"]').val('');
        setTimeout(() => {
            $parent.find('.replied-message__text').text('');
        }, 200);
        
    });

    $('.comments-group').on('click', 'button.comment-reply', function() {
        const $this = $(this);
        const id = $this.attr('data-id');
        const commentText = $this.closest('.comment-group__item').find('.comment-content_origin').text();
        formComment.find('[name="reply"]').val(id);
        $('.replied-message__text').text(commentText);
        $('.replied-message').slideDown(200);
        $('html, body').stop().animate({
            scrollTop: formComment.offset().top - 150
        }, 300);
        if (!formComment.find('[name="name"]').val()) {
            formComment.find('[name="name"]').focus(); 
        } else if (!formComment.find('[name="surname"]').val()) {
            formComment.find('[name="surname"]').focus(); 
        } else {
            formComment.find('[name="msg"]').focus(); 
        }
    });

    formComment.on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        const url = form.attr('action');
        const data = form.serialize();
        const $btn = form.find('[type="submit]');
        const name = form.find('[name="name"]').val();
        const surName = form.find('[name="surname"]').val();
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            beforeSend: function() {
                $btn.prop('disabled', true);
            },
            success: function(response) {
                $btn.prop('disabled', false);
                form.find('textarea').val('');
                if (response.status === 'ok') {
                    appendComment(response);
                    $('.delete-replied-comment').click();
                    localStorage.setItem('name', name);
                    localStorage.setItem('surname', surName);
                }
            },
        });
    });

    function appendComment(response) {
        let comment = $(parseData(response.data));
        comment.hide();
        $('.comments-group').append(comment);
        comment.slideDown(200);
        $('.comments__cnt').text(+$('.comments__cnt').text() + 1);
    }

    function parseData(data) {
        let template;
        if (data.replied_comment) {
            template = `
            <li id="comment-${data.id}" class="comment-group__item comment">
                <div class="comment-wrapper">
                    <p class="comment__author">
                        <span>Автор: ${data.full_name}</span>
                    </p>
                    <div class="comment__date">
                        <span>Дата: </span>
                        <time>${formatDate(data.time)}</time>
                    </div>
                    <a href="#comment-${data.replied_comment.id}" class="comment__cite">
                        <p class="comment__author">
                            <span>От пользователя: ${data.replied_comment.full_name}</span>
                        </p>
                        <div class="comment__date">
                            <span>Дата: </span>
                            <time>${formatDate(data.replied_comment.time)}</time>
                            <p class="comment-content">
                                ${data.replied_comment.msg}
                            </p>
                        </div>
                    </a>
                    <p class="comment-content comment-content_origin">
                    ${data.msg}
                    </p>

                    <button class="comment-reply" type="button" data-id="${data.id}">Ответить</button>
                </div>
            </li>
            `;
        } else {
            template = `
            <li id="comment-${data.id}" class="comment-group__item comment">
                <div class="comment-wrapper">
                    <p class="comment__author">
                        <span>Автор: ${data.full_name}</span>
                    </p>
                    <div class="comment__date">
                        <span>Дата: </span>
                        <time>${formatDate(data.time)}</time>
                    </div>
                    <p class="comment-content comment-content_origin">
                    ${data.msg}
                    </p>

                    <button class="comment-reply" type="button" data-id="${data.id}">Ответить</button>
                </div>
            </li>
            `;
        }

        return template;
    }

    function formatDate(date) {
        let d = new Date(date);
        date = [
            ('0' + d.getDate()).slice(-2),
            ('0' + (d.getMonth() + 1)).slice(-2),
            d.getFullYear()
          ].join('.');
        return date;
    }

    // send mail
    $('.feadback-form').submit(function(e) {
        e.preventDefault();
        const form = $(this);
        const $btn = form.find('[type="submit"]');
        const url = form.attr('action');
        data = form.serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            beforeSend: function() {
                $btn.prop('disabled', true).find('span').text('Отправка ⌛');
            },
            success: function(response) {
                if (response.status === 'ok') {
                    $btn.find('span').text('Отправлено ✔');
                } else {
                    $btn.find('span').text('Ошибка ✖');
                }
            },
        });
    });
});
// end ready
