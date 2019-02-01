$(function () {

    init();


    function registRemoveAction(dom, url) {
        if (!url) {
            url = 'remove';
        }
        if (dom) {
            dom.unbind('click')
            dom.on('click', function() {
                var id = $(this).parent().attr('id')
                post(url, {'id': id}, null, function(data) {
                    if (data === 'ok') {
                        $('#'+id).remove()
                    } else {
                        alert('Remove failed. Try later.')
                    }
                })
            })
        }
    }

    function registRemoveActionLocal(dom, ln) {
        if (dom) {
            dom.unbind('click')
            dom.on('click', function() {
                var v = $(this).prev().text();
                var old = $('#'+ln).data('expr_arr');
                if (old && $.isArray(old)) {
                    var newArr = old.slice();
                    var idx = newArr.indexOf(v);
                    if (idx > -1) {
                        newArr.splice(idx, 1);
                    }
                    $('#'+ln).data('expr_arr', newArr);
                } else {
                    $('#'+ln).data('expr_arr', []);
                }
                $(this).parent().remove();

            })
        }
    }

    function registEditAction(dom) {
        if (dom) {
            dom.unbind('click')
            dom.on('click', function() {
                var id = $(this).parent().attr('id')
                post('find', {'id': id}, null, function(data) {
                    if (data) {
                        var obj = JSON.parse(data);
                        fillBlanks(obj)
                    } else {
                        alert('Error: cannot get the word from db.')
                    }
                })
            })
        }
    }

    function post(url, p, errmsg, fnc) {
        var token = getToken();
        if (fnc) {
            $.post(url, $.extend({},token,p), function(data) {fnc(data)})
        } else {
            $.post(url, $.extend({},token,p), function(data) {if (data !== 'ok') alert(errmsg);})
        }
    }

    function getToken() {
        var obj = $('#token input:first');
        var ret = {}
        ret[obj.attr('name')] = obj.val()
        return ret;
    }

    function init() {
        $('#subject').children().eq(0).attr('selected', 'selected')

        $('#expr_exist').hide()

        bindBtnEvent()

        showAllSubject()
    }

    function showAllSubject() {
        $('#sbj_list').empty()
        post('search_subject', {}, null, function(data) {
            if (!data) return
            var arr = JSON.parse(data)
            if (!arr) return
            var ul = $('<ul class="data_list"></ul>')
            ul.append('<li class="head_row"><span>Subject Name</span><span>Operation</span></li>')
            for (var i in arr) {
                ul.append('<li id="'+arr[i]._id['$oid']+'"><span>'+arr[i].eng_name+'</span><span class="remove">[X]</span></li>')
            }
            $('#sbj_list').append(ul);
            registRemoveAction($('#sbj_list ul li span.remove'), 'remove_subject')
        })
    }

    function setSSP(vn, ln) {
        var s_sp = $('#'+vn).val();
        var s_sp_arr = $('#'+ln).data('expr_arr')
        if (s_sp) {
            if (s_sp_arr && $.isArray(s_sp_arr)) {
                var tmp_arr = s_sp.split(',')
                for (var i in tmp_arr) {
                    if (s_sp_arr.indexOf(tmp_arr[i]) < 0) {
                        s_sp_arr.push(tmp_arr[i]);
                    }
                }

                s_sp_arr.sort(function(a, b) {return a.localeCompare(b);});
            } else {
                s_sp_arr = [];
                var tmp_arr = s_sp.split(',')
                for (var i in tmp_arr) {
                    s_sp_arr.push(tmp_arr[i]);
                }
            }
        }
        if (s_sp_arr && $.isArray(s_sp_arr)) {
            return s_sp_arr.join(',');
        }
        return '';
    }

    function bindBtnEvent() {
        $('#save_btn').click(function() {
            var param = {}
            var inputs = ['expr', 'trans', 'subject', 'tag']
            for (var x in inputs) {
                param[inputs[x]] = $('#'+inputs[x]).val();
            }
            param['example'] = $('#example').val()
            param['synonym'] = setSSP("synonym", "synonym_list");
            param['similar_spelling'] = setSSP("similar_spelling", "similar_spelling_list");
            console.log(param)
            post('save', param, null, function(data) {
                if (data === 'ok') {
                    resetForm();
                } else {
                    alert('save fail ')
                }
            } )
        })
        $('#search_btn').click(function() {
            $('#search_result').empty();
            var str = $('#search').val()
            if (!str) {
                alert('search string should not be empty');
            }
            post('search', {'expr': str}, null, function(data) {
//                console.log(data)
                var json = JSON.parse(data)
                if (json) {
                    var ul = $('<ul class="data_list"></ul>')
                    ul.append('<li class="head_row"><span>Expression</span><span>Translation</span><span>Tag</span><span class="long_txt">Example</span><span>Subject</span><span>Operation</span></li>')
                    for (var i in json) {
                        ul.append('<li id="'+json[i]._id['$oid']+'"><span>'+json[i].expr+'</span><span>'+json[i].trans+'</span><span>'+json[i].tag+'</span><span class="long_txt">'+json[i].example+'</span><span>'+json[i].subject+'</span><span class="edit">[E]</span><span class="remove">[X]</span></li>')
                    }
                    $('#search_result').append(ul);
                }

                registRemoveAction($('#search_result ul li span.remove'))
                registEditAction($('#search_result ul li span.edit'))
            })
        })

        $("#sbj_save_btn").click(function() {
            post('save_subject', {"eng_name": $('#subject_name').val()}, 'save subject fail.Please try later.')
            showAllSubject()
        })

        $('#expr').blur(function() {
            $('#expr_exist').hide()
            var expr = $(this).val()
            post('search', {'type':'eq','expr': expr}, null, function(data) {
//                console.log(data)
                if (data) {
                    var json = JSON.parse(data)[0]
                    if (json) {
                        $('#expr_exist').text('exist')
                        $('#expr_exist').show()
                        fillBlanks(json)
                    }
                } else {
                    $('#expr_exist').empty()
                }
            })
        })
    }

    function fillBlanks(obj) {
        if (!obj) {
            return;
        }
        $('#expr').val(obj.expr)
        $('#trans').val(obj.trans)
        $('#subject').val(obj.subject)
        $('#tag').val(obj.tag)
        $('#example').val(obj.example)
        $('#synonym').val('')
        $('#similar_spelling').val('')

        refreshWordList('synonym_list', obj.synonym)
        refreshWordList('similar_spelling_list', obj.similar_spelling)

    }

    function resetForm() {
        $('#expr').val('')
        $('#trans').val('')
        $('#subject').val('')
        $('#tag').val('')
        $('#example').val('')
        $('#synonym').val('')
        $('#similar_spelling').val('')
        $('#synonym_list').empty()
        $('#similar_spelling_list').empty()
    }

    function refreshWordList(dom_id, str) {
        var dom = $('#'+dom_id)
        dom.empty()
        if (!str) {
            return;
        }
        var arr = str.split(',')
        var n_arr = []
        $ul = $('<ul class="data_list"></ul>')
        for (var i in arr) {
            var s = arr[i].trim()
            if (!s) {
                continue;
            }
            n_arr.push(s)
            $ul.append('<li><span>'+s+'</span><span class="remove">[X]</span></li>')
        }
        dom.data('expr_arr', n_arr)
        dom.append($ul)
        registRemoveActionLocal($ul.find('span.remove'), dom_id)
    }

})