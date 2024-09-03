from flask import url_for

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"

def validate_character(payload):
    errors = dict()
    missing_keys = set(["name", "height", "mass"])
    optional_keys = set(["homeworld_id", "eye_color_id", "hair_color_id", "skin_color_id", "gender_id", "birth_year"])
    extra_keys = []

    for key in payload:
        value = payload[key]
        if key in missing_keys:
            if key == "name":
                if not isinstance(value, str):
                    errors["name"] = "The name should be a string"
                elif len(value) == 0:
                    errors["name"] = "The name should be a non empty string"
                missing_keys.remove("name")
            else:
                if not isinstance(value, float) and not isinstance(value, int):
                    errors[key] = f"The {key} should be a real number"
                elif value < 0:
                    errors[key] = f"The {key} should be a non negative number"
                missing_keys.remove(key)
        elif key in optional_keys:
            if key == "birth_year":
                if not isinstance(value, str):
                    errors["name"] = "The birth year should be a string"
                elif len(value) == 0:
                    errors["name"] = "The birth year should be a non empty string"
            else:
                if not isinstance(value, int):
                    errors[key] = f"The {key} should be an integer"
        else:
            extra_keys.append(key)
        
    if len(missing_keys) > 0:
        errors["missing_keys"] = ",".join(missing_keys)
    
    if len(extra_keys) > 0:
        errors["extra_keys"] = ",".join(extra_keys)
    
    return (not bool(errors), errors)

def validate_color(payload):
    errors = dict()
    missing_keys = set(["name"])
    extra_keys = []
    
    for key in payload:
        value = payload[key]
        if key == "name":
            if not isinstance(value, str):
                errors["name"] = "The name should be a string"
            elif len(value) == 0:
                errors["name"] = "The name should be a non empty string"
            missing_keys.remove("name")
        else:
            extra_keys.append(key)
    
    if len(missing_keys) > 0:
        errors["missing_keys"] = ",".join(missing_keys)
    
    if len(extra_keys) > 0:
        errors["extra_keys"] = ",".join(extra_keys)
    
    return (not bool(errors), errors)

def validate_gender(payload):
    return validate_color(payload)

def validate_planet(payload):
    errors = dict()
    missing_keys = set(["name", "rotation_period", "orbital_period", "gravity", "diameter", "surface_water", "population"])
    extra_keys = []
    
    for key in payload:
        value = payload[key]
        if key == "name":
            if not isinstance(value, str):
                errors["name"] = "The name should be a string"
            elif len(value) == 0:
                errors["name"] = "The name should be a non empty string"
            missing_keys.remove("name")
        elif key == "rotation_period" or key == "orbital_period" or key == "diameter":
            if not isinstance(value, float) and not isinstance(value, int):
                errors[key] = f"The {key} should be a real number"
            elif value <= 0:
                errors[key] = f"The {key} should be positive"
            missing_keys.remove(key)
        elif key == "gravity":
            if not isinstance(value, float) and not isinstance(value, int):
                errors["gravity"] = "The gravity should be a real number"
            elif value < 0:
                errors["gravity"] = "The gravity should be a non negative number"
            missing_keys.remove("gravity")
        elif key == "surface_water":
            if not isinstance(value, float) and not isinstance(value, int):
                errors["surface_water"] = "The surface water should be a real number"
            elif value < 0 or value > 100:
                errors["surface_water"] = "The surface water should be a real number in [0, 100]"
            missing_keys.remove("surface_water")
        elif key == "population":
            if not isinstance(value, int):
                errors["population"] = "The population should be an integer"
            elif value < 0:
                errors["population"] = f"The population should be a non negative integer"
            missing_keys.remove("population")
        else:
            extra_keys.append(key)
    
    if len(missing_keys) > 0:
        errors["missing_keys"] = ",".join(missing_keys)
    
    if len(extra_keys) > 0:
        errors["extra_keys"] = ",".join(extra_keys)
    
    return (not bool(errors), errors)