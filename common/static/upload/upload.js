

var uploadPath = '/common/upload/';

$(function ($) {
    if(window.django && window.django.jQuery){
        $ = django.jQuery;
        if(!window.$){ // 系统把全局得 $ 去掉了，要把这个 全局到设置到 window
            window.$ = django.jQuery;
        }
    }

    if(!$ && jQuery){
        window.$ = jQuery;
    }

    var imageType = 'image/jpeg , image/png , image/gif'
    $(document).on('click', '.file-upload-box', function (e) {
        var target = e.target;
        var $this = $(this);
        if($this.hasClass('upload-status'))return;
        if ($(target).hasClass('close')) {
            // 关闭
            if($this.data('mul')){
                $this.remove();
                updateImagesList($this.parents('.file-upload-list'));
            }else{
                $(this).addClass('empty-file');
                $(this).find('input').val('');
                $(this).find('.thumb img').attr('src' , '');
            }
        } else {
            var that = this;
            openSelectFile(this , function (files){
                sendAndInsertImage(that, files[0] , function (eventName, res ){
                    if(eventName == 'success'){
                        $this.find('.thumb img').attr('src' , res.url);
                        $(that).removeClass('empty-file');
                        $this.find('input').val(res.url);

                        if($this.data('mul')){
                            updateImagesList($this.parents('.file-upload-list'))
                        }
                    }
                });
            },imageType);
        }
    });

    $(document).on('click' , '.file-list-btn-upload' , function (e){
        var that = $(this);
        var parents = that.parents('.file-upload-list');
        var fileList = parent.find('.file-upload-list-box');
        openSelectFile(this, function (files){
            $.each(files , function (i , file){
                var tpl = createUploadFileTpl(parents.data('name'));
                fileList.append(tpl);
                sendAndInsertImage(tpl, file , function (eventName, res ){
                    if(eventName == 'success'){
                        tpl.find('.thumb img').attr('src' , res.url);
                        tpl.removeClass('empty-file');
                        updateImagesList(parents);
                    }
                });
            });
        },imageType,true);
    });

    $('.file-upload-image').each(function (){
        var that = $(this);
        var src = that.find('input').val();
        if(src){
            that.find('.thumb>img').attr('src' , src);
            that.removeClass('empty-file')
        }else{
            that.addClass('empty-file')
        }
    });

    $('.file-upload-list').each(function (){
        var that = $(this);
        var jsonData = that.find('input').val();
        try{
            var images = JSON.parse(jsonData);
            $.each(images , function (i,src){
                var tpl = createUploadFileTpl('_a' ,src);
                that.find('.file-upload-list-box').append(tpl);
            });
        }catch (e){
            that.find('input').val('[]');
        }
    });



    function updateImagesList( obj ){
        var result = [];
        $(obj).find('.file-upload-box').each(function (){
            var src = $(this).find('.thumb img').attr('src');
            result.push(src);
        });
        $(obj).find('input').val(JSON.stringify(result));
    }

});

function createUploadFileTpl( name ,  src  )
{
    src = src || '';
    var tpl = '<div class="file-upload-box file-upload-image file-upload-box-2x '+(src?'':'empty-file')+'" data-mul="true" data-image="true" data-url="/">\n' +
        '    <div class="thumb">\n' +
        '        <img src="'+src+'"/>\n' +
        '    </div>\n' +
        '    <a href="javascript:;" class="close">╳</a>\n' +
        '    <div class="upload-btn">\n' +
        '        <span>\n' +
        '            上传图片\n' +
        '        </span>\n' +
        '    </div>\n' +
        //     '    <input type="text" name="'+name+'" style="display: none" value="'+(src instanceof String ? src : '')+'"/>\n' +
        '</div>';
    return $(tpl);
}


function openSelectFile(target  , callback , accept , isMul)
{
    var form = $(target).data('form')
    var input = $(target).data('input')
    if (!form) {
        form = document.createElement('form')
        form.action = 'javascript:;'
        input = document.createElement('input')
        input.type = 'file'
        if(isMul) input.multiple = 'multiple';
        if(accept) input.accept = accept;
        form.appendChild(input)
        $(target).data('form', form)
        $(target).data('input', input)
        $(input).change(function (e) {
            var files = e.target.files;
            if (files.length > 0) {
                callback && callback(files);
            }
        });
    }
    form.reset();
    input.click();
}

/**
 * ajax方式发送文件
 * @param file
 */
function sendAndInsertImage(fileUpload, file , callback) {

    $(fileUpload).addClass('upload-status');
    var statusSpan = $(fileUpload).find('.upload-btn span');
    var sourceHtml = statusSpan.html();
    statusSpan.html('Uploading...');
    //构建模拟数据
    var fd = new FormData();
    //  设置fujian 文件
    fd.append('upfile', file, file.name || ('blob.' + file.type.substr('image/'.length)));
    //  设置 类型为 ajax
    fd.append('type', 'ajax');
    // 创建ajax 对象
    var xhr = new XMLHttpRequest();
    // 设置为post 提交
    xhr.open("post", uploadPath, true);
    // 设置提交头
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.upload.addEventListener('progress', function (e) {
        var total = e.total;
        var loaded = e.loaded;
        if(total == 0 || isNaN(total))return;
        var progress = ((loaded / total) * 100).toFixed(2);
        statusSpan.html('已上传'+(progress)+'%');
        callback && callback('progress' , {
            total: total,
            loaded: loaded,
            progress:progress
        });
    });
    // 加载完成后，返回数据
    xhr.addEventListener('load', function (e) {
        try {
            // 将结果写入 body 中
            var data = e.target.response
            // 获取json 数据
            $(fileUpload).removeClass('upload-status')
            statusSpan.html(sourceHtml);

            var result = eval('(' + data + ')');
            if(result.state == 'SUCCESS'){
                $(fileUpload).find('input').val(result.url);
                callback && callback('success' , result);
            }else{
                callback&&callback('error' , {
                    msg:'文件上传错误'
                })
            }
        } catch (er) {
            callback&&callback('error' , {
                msg:'文件上传错误'
            })
        }
    });
    xhr.send(fd);
}

