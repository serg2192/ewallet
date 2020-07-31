from billing.resources import views


def set_routes(app):
    router = app.router

    create_account_resource = router.add_resource(
        '/create_account', name='create_account'
    )
    create_account_resource.add_route(
        'POST',
        views.create_account
    )

    add_money_resource = router.add_resource(
        '/add_money', name='add_money'
    )
    add_money_resource.add_route(
        'POST',
        views.add_money
    )

    transfer_resource = router.add_resource(
        '/transfer', name='transfer'
    )
    transfer_resource.add_route(
        'POST',
        views.transfer
    )
