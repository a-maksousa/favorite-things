$(document).ready(function () {

    $(".preloader").hide();

    $(document).ajaxStart(function () {
        $(".preloader").show();
    });

    $(document).ajaxStop(function () {
        $(".preloader").hide();
    });

    $(document).tooltip();

    window.onload = function () {
        var reloading = sessionStorage.getItem("ReloadingMessage");
        if (reloading) {
            this.ShowMessage(reloading)
            sessionStorage.removeItem("ReloadingMessage");
        }
    }

    $("#addCategoryModal").submit(function (event) {
        event.preventDefault();
        submitForm();
    });

    window.addEventListener('load', function () {
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);

    $(".btnDeleteCat").click(function () {
        intCatID = $(this).parents()[2].id;
        Swal.fire({
            title: 'Are you sure?',
            text: "All Favorite Items for this Category will be Deleted !",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes'
        }).then((result) => {
            if (result.value) {
                $.post('/DeleteCategory', {
                    id: intCatID
                }).done(function (response) {
                    if (response.code == 0) {
                        ShowError(response.msg)
                    }
                    else {
                        location.reload();
                        sessionStorage.setItem("ReloadingMessage", "Category is Deleted Successfully");
                    }
                })
            }
        })
    })

    $("#btnClearLogs").click(function () {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes'
        }).then((result) => {
            if (result.value) {
                $.post('/ClearLogs').done(function (response) {
                    if (response.code == 0) {
                        ShowError(response.msg)
                    }
                    else {
                        $("#tblLogs").jsGrid("option", "data", []);
                        ShowMessage("Logs Cleared Successfully")
                    }
                })
            }
        })
    })

});

function InitFavGrid(intCatID) {
    $.get('/GetFavByCatID', {
        intCategoryID: intCatID
    }).done(function (response) {
        if (response.code == 0) {
            ShowError(response.msg)
        }
        else {
            $("#favorites_" + intCatID).jsGrid({
                width: "100%",
                inserting: true,
                editing: true,
                sorting: true,
                paging: true,
                confirmDeleting: false,
                data: response.data,
                invalidNotify: function (args) {
                    ShowError("Please fill all required fields")
                },
                fields: [
                    { name: "intFavID", visible: false },
                    { name: "title", title: "Title", type: "text", validate: "required" },
                    { name: "description", title: "Description", type: "text" },
                    { name: "ranking", title: "Rank", type: "number", validate: "required", editing: false, align: "center" },
                    { name: "cteated_date", title: "Created Date" },
                    { name: "modified_date", title: "Modified Date" },
                    {
                        title: "Meta Data", align: "center",
                        itemTemplate: function (_, item) {
                            return $("<div class='meta_Data_icon'><i class='fas fa-info-circle'</i></div>")
                                .on("click", function (e) {
                                    InitMetaDataGrid(item.id)
                                });
                        }
                    },
                    { type: "control" }
                ],
                onItemInserted: function (args) {
                    $.post('/AddFavByCatID', {
                        intCatID: intCatID,
                        strFavoriteTitle: args.item.title,
                        strDescription: args.item.description,
                        intRanking: args.item.ranking
                    }).done(function (response) {
                        if (response.code == 0) {
                            args.item.deleteConfirmed = true;
                            $("#favorites_" + intCatID).jsGrid("deleteItem", args.item);
                            ShowError(response.msg)
                        }
                        else {
                            $.get('/GetFavByCatID', {
                                intCategoryID: intCatID
                            }).done(function (response) {
                                $("#favorites_" + intCatID).jsGrid("option", "data", response.data)
                            });

                            ShowMessage("Favorite is Added Successfully")
                        }
                    })
                },
                onItemDeleting: function (args) {
                    if (!args.item.deleteConfirmed) {
                        args.cancel = true;
                        Swal.fire({
                            title: 'Are you sure?',
                            text: "You won't be able to revert this!",
                            type: 'warning',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes'
                        }).then((result) => {
                            if (result.value) {
                                args.item.deleteConfirmed = true;
                                $.post('/DeleteFavorite', {
                                    intFavID: args.item.id
                                }).done(function (response) {
                                    if (response.code == 0) {
                                        ShowError(response.msg)
                                    }
                                    else {
                                        $("#favorites_" + intCatID).jsGrid("deleteItem", args.item);
                                        ShowMessage("Favorite is Added Successfully")
                                    }
                                })
                            }
                        })
                    }
                },
                onItemUpdated: function (args) {
                    $.post('/UpdateFavorite', {
                        intFavID: args.item.id,
                        strTitle: args.item.title,
                        strDescription: args.item.description,
                        intRank: args.item.ranking
                    }).done(function (response) {
                        if (response.code == 0) {
                            ShowError(response.msg)
                        }
                        else {
                            $.get('/GetFavByCatID', {
                                intCategoryID: intCatID
                            }).done(function (response) {
                                $("#favorites_" + intCatID).jsGrid("option", "data", response.data)
                            });

                            ShowMessage("Favorite is Updated Successfully")
                        }
                    })
                }
            });
        }
    })
}

function InitMetaDataGrid(intFavID) {
    $.get('/GetMetaDataByFavID', {
        intFavoriteID: intFavID
    }).done(function (response) {
        if (response.code == 0) {
            ShowError(response.msg)
        }
        else {
            $('#metaData').modal('show');
            $(".jsgrid-cancel-edit-button").click()
            $("#metaDataGrid").jsGrid({
                width: "100%",
                inserting: true,
                editing: true,
                sorting: true,
                paging: true,
                confirmDeleting: false,
                data: response.data,
                invalidNotify: function (args) {
                    ShowError("Please fill all required fields")
                },
                fields: [
                    { name: "intMetaDataID", visible: false },
                    { name: "key", title: "Key", type: "text", validate: "required" },
                    { name: "value", title: "Value", type: "text", validate: "required" },
                    { type: "control" }
                ],
                onItemInserted: function (args) {
                    $.post('/AddMetaData', {
                        intFavID: intFavID,
                        key: args.item.key,
                        value: args.item.value
                    }).done(function (response) {
                        if (response.code == 0) {
                            args.item.deleteConfirmed = true;
                            $("#metaDataGrid").jsGrid("deleteItem", args.item);
                            ShowError(response.msg)
                        }
                        else {
                            $.get('/GetMetaDataByFavID', {
                                intFavoriteID: intFavID
                            }).done(function (response) {
                                $("#metaDataGrid").jsGrid("option", "data", response.data)
                            });

                            ShowMessage("MetaData is added successfully")
                        }
                    })
                },
                onItemDeleting: function (args) {
                    if (!args.item.deleteConfirmed) {
                        args.cancel = true;
                        Swal.fire({
                            title: 'Are you sure?',
                            text: "You won't be able to revert this!",
                            type: 'warning',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes'
                        }).then((result) => {
                            if (result.value) {
                                args.item.deleteConfirmed = true;
                                $.post('/DeleteMetaData', {
                                    intFavID: intFavID,
                                    intMetaDataID: args.item.id
                                }).done(function (response) {
                                    if (response.code == 0) {
                                        ShowError(response.msg)
                                    }
                                    else {
                                        $("#metaDataGrid").jsGrid("deleteItem", args.item);
                                        ShowMessage("MetaData has been Removed successfully")
                                    }
                                })
                            }
                        })
                    }
                },
                onItemUpdated: function (args) {
                    $.post('/UpdateMetaData', {
                        intFavID: intFavID,
                        intMetaDataID: args.item.id,
                        key: args.item.key,
                        value: args.item.value
                    }).done(function (response) {
                        if (response.code == 0) {
                            ShowError(response.msg)
                        }
                        else {
                            ShowMessage("MetaData has been Updated successfully")
                        }
                    })
                }
            });
        }
    })
}

function InitLogsGrid() {
    $.get('/GetLogs').done(function (response) {
        if (response.code == 0) {
            ShowError(response.msg)
        }
        else {
            $("#tblLogs").jsGrid({
                width: "100%",
                inserting: false,
                editing: false,
                sorting: true,
                paging: true,
                confirmDeleting: false,
                data: response.data,

                fields: [
                    { name: "description", title: "Description", type: "text" },
                    { name: "log_date", title: "Date", type: "text" },
                ]
            });
        }
    })
}

function ShowMessage(msg) {
    $.toast({
        text: msg,
        position: 'top-left',
        icon: "success",
        loader: false,
        stack: false
    })
}

function ShowError(msg) {
    $.toast({
        text: msg,
        position: 'top-left',
        icon: "error",
        loader: false,
        stack: false
    })
}

function submitForm() {
    var strTitle = $("#strCategoryTitle").val();
    $.post('AddCategory', {
        strCategoryTitle: strTitle
    }).done(function (response) {
        if (response.code == 0) {
            ShowError(response.msg)
        }
        else {
            location.reload()
            sessionStorage.setItem("ReloadingMessage", "Category is Added Successfully");
        }
    })
}