from apps.commons.breadcrumbs import BreadCrumb


def bc_learn():
    return BreadCrumb('Aprender', 'learn:index')


def bc_label(label):
    return bc_learn().step(
        label,
        'learn:resources_by_label',
        label,
        )
