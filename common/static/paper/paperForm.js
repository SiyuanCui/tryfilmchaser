(function ($){
    function PaperForm(option){
        this.$el = $(option.el);
        this.$type = $(option.type);
        var defaults = {
            danxuanti:'单选题',
            duoxuanti:'多选题',
            panduanti:'判断题'
        };
        this.options = $.extend(true , {} , defaults , option);
        this.initTemplate();
        this.initEvent();
        this.init();
    }
    PaperForm.prototype = {
        init:function(){
            var that = this;
            var value = this.$el.val();
            try{
                var data = eval('('+value+')');
                if($.isArray(data)){
                    $.each(data , function (i,o){
                        that.addItem(o);
                    });
                }
            }catch (e){

            }
        },
        initEvent:function (){
            var that = this;
            this.$tpl.find('#add_btn').click(function (){
                that.addItem();
            });
            this.$tpl.on('click' , '.btn-close' , function (e){
                if (confirm('此操作将不可恢复，您确定删除？')) {
                    $(this).parent().parent().remove();
                }
                that.updateZimu();
                that.updateData();
            });
            this.$tpl.on('blur' , 'input' , function (e) {
                that.updateData();
            });
            this.$type.on('change' , function (){
                that.selectType(this);
            });
            var form = this.$el.parents('form');
            if(form.length > 0){
                form.on('submit' , function (){
                    that.updateData();
                    return true;
                });
            }
        },
        selectType:function (obj) {
            var v = $(obj).val();
            if ( this.isShowSelected(v) ) {
                this.$tpl.find('#TypeFieldabc').show();
            } else {
                this.$tpl.find('#TypeFieldabc').hide();
            }
        },
        isShowSelected:function( type ){
            var option = this.options;
            return option.danxuanti.indexOf(type) !== -1 || option.duoxuanti.indexOf(type)!==-1 || option.panduanti.indexOf(type) !== -1
        },
        updateZimu:function () {
            var zimu = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            var index = this.$tpl.find("#field_box").find("tr").each(function (index) {
                $(this).find('td:eq(0)').find('input').val(zimu.substr(index, 1));
            });
        },
        updateData: function () {
            var result = [];
            this.$tpl.find('#field_box').find('tr').each(function () {
                var obj = {};
                $(this).find('[data-id]').each(function () {
                    if ($(this).attr('type') == 'checkbox') {
                        obj[$(this).attr('data-id')] = $(this).attr('checked')
                    } else {
                        obj[$(this).attr('data-id')] = $.trim($(this).val());
                    }
                });
                if (obj.title != '' && obj.point != '') {
                    result.push(obj);
                }
            });
            this.$el.val(JSON.stringify(result));
        },
        addItem:function(wx){
            wx = wx || {};
            var that = this;
            var str = [];
            str.push('<tr><td align="center" valign="middle">');
            str.push('<input type="text" readonly="readonly" style="width: 40px;" data-id="zimu" class="form-control" value="" />');
            str.push('</td><td>');
            str.push('<input type="text" style="width:100%" data-id="title" class="form-control" value="' + (wx.title || '') + '" />');
            str.push('</td><td>');
            str.push('<input type="number" step="1" style="width: 60px;" data-id="point" class="form-control" value="' + (wx.point || '0') + '" />');
            str.push('</td><td>');
            str.push('<button type="button" class="btn btn-default btn-close">删除</button>');
            str.push('</td></tr>');
            var html = str.join('');
            this.$tpl.find('#field_box').append(html);
            that.updateZimu();
        },
        initTemplate:function (){
            var str = '<div id="TypeFieldabc">\n' +
            '                    <div style="border: 1px solid #ededed; border-radius: 5px; padding: 10px; background: #F2F2F2;">\n' +
            '                        <table class="table table-hover">\n' +
            '                            <thead>\n' +
            '                            <tr>\n' +
            '                                <th width="80">&nbsp;</th>\n' +
            '                                <th>答案</th>\n' +
            '                                <!--<th width="80">跳转序号</th>-->\n' +
            '                                <th width="60">得分</th>\n' +
                '<th></th>'+
            '                            </tr>\n' +
            '                            </thead>\n' +
            '                            <tbody id="field_box">\n' +
            '                            \n' +
            '                            </tbody>\n' +
            '                        </table>\n' +
            '                    </div>\n' +
            '                    <button type="button" class="btn btn-default btn-sm" id="add_btn" >增加答案</button>\n' +
            '                </div>';

            this.$tpl = $(str);
            this.$el.after(this.$tpl);
        }
    };

    window.PaperForm = PaperForm;
    return PaperForm
})(jQuery);
