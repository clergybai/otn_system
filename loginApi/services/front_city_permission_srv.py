from ..models.front_city_permission import FrontCityPermission


def get_city_permissions(distinct_field, field_list, **filters):
    return FrontCityPermission.get_by(distinct_field, field_list, **filters)


def get_all_cities():
    results = FrontCityPermission.get_cities()
    return [item[0] for item in results]
