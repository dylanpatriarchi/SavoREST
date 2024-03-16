import os
import subprocess
import re

def create_lumen_project(project_name):
    subprocess.run(["php", "composer.phar", "create-project", "--prefer-dist", "laravel/lumen", project_name])

def parse_resources_and_accounts(file_content):
    resources_pattern = r'resources\{([^}]*)\}'
    accounts_pattern = r'accounts\{([^}]*)\}'

    resources_match = re.search(resources_pattern, file_content, re.DOTALL)
    accounts_match = re.search(accounts_pattern, file_content, re.DOTALL)

    if resources_match:
        resources_content = resources_match.group(1).strip()
        resources = parse_resource_definitions(resources_content)
    else:
        resources = {}

    if accounts_match:
        accounts_content = accounts_match.group(1).strip()
        accounts = parse_account_definitions(accounts_content)
    else:
        accounts = []

    return resources, accounts

def parse_resource_definitions(resources_content):
    resource_pattern = r'define_resource:\s+(\w+)\s+\[(.*?)\]\s+&&\s+(\w+)\s+&&\s+(\w+)'
    resource_definitions = {}

    for match in re.finditer(resource_pattern, resources_content):
        resource_name = match.group(1)
        permissions_str = match.group(2)
        permissions = {}
        for perm in permissions_str.split(','):
            key, value = perm.strip().split('=')
            permissions[key.strip()] = value.strip()
        uri_name = match.group(3)
        table_name = match.group(4)
        resource_definitions[resource_name] = {
            'permissions': permissions,
            'uri': uri_name,
            'table': table_name
        }

    return resource_definitions

def parse_account_definitions(accounts_content):
    account_pattern = r'define_account:\s+(\w+),\s+(\w+),\s+(\w+),\s+(\w+)'
    account_definitions = []

    for match in re.finditer(account_pattern, accounts_content):
        account_name = match.group(1)
        roles = match.group(2).split(',')
        password = match.group(3)
        email = match.group(4)
        account_definitions.append({
            'name': account_name,
            'roles': roles,
            'password': password,
            'email': email
        })

    return account_definitions

def generate_lumen_code(resources):
    route_code = "<?php\n\n"
    controller_code = {}
    model_code = "<?php\n\n"
    
    for resource_name, resource_data in resources.items():
        uri = resource_data['uri']
        table_name = resource_data['table']
        permissions = resource_data['permissions']
        
        # Route
        route_code += f"$router->group(['prefix' => '{uri}'], function () use ($router) {{\n"
        if permissions.get('READ', True):
            route_code += f"    $router->get('/', '{resource_name.capitalize()}Controller@index');\n"
        if permissions.get('CREATE', True):
            route_code += f"    $router->post('/', '{resource_name.capitalize()}Controller@store');\n"
        if permissions.get('READ', True):
            route_code += f"    $router->get('/{{id}}', '{resource_name.capitalize()}Controller@show');\n"
        if permissions.get('UPDATE', True):
            route_code += f"    $router->put('/{{id}}', '{resource_name.capitalize()}Controller@update');\n"
        if permissions.get('DELETE', True):
            route_code += f"    $router->delete('/{{id}}', '{resource_name.capitalize()}Controller@destroy');\n"
        route_code += "});\n\n"
        
        # Controller
        controller_code[resource_name] = "<?php\n\n"
        controller_code[resource_name] += f"namespace App\\Http\\Controllers;\n\n"
        controller_code[resource_name] += f"use App\\Models\\{resource_name.capitalize()};\n"
        controller_code[resource_name] += "use Illuminate\\Http\\Request;\n\n"
        controller_code[resource_name] += f"class {resource_name.capitalize()}Controller extends Controller\n"
        controller_code[resource_name] += "{\n"
        if permissions.get('READ', True):
            controller_code[resource_name] += f"    public function index()\n"
            controller_code[resource_name] += "    {\n"
            controller_code[resource_name] += f"        return response()->json({resource_name.capitalize()}::all());\n"
            controller_code[resource_name] += "    }\n\n"
        if permissions.get('CREATE', True):
            controller_code[resource_name] += f"    public function store(Request $request)\n"
            controller_code[resource_name] += "    {\n"
            controller_code[resource_name] += f"        return response()->json({resource_name.capitalize()}::create($request->all()), 201);\n"
            controller_code[resource_name] += "    }\n\n"
        if permissions.get('READ', True):
            controller_code[resource_name] += f"    public function show($id)\n"
            controller_code[resource_name] += "    {\n"
            controller_code[resource_name] += f"        return response()->json({resource_name.capitalize()}::find($id));\n"
            controller_code[resource_name] += "    }\n\n"
        if permissions.get('UPDATE', True):
            controller_code[resource_name] += f"    public function update(Request $request, $id)\n"
            controller_code[resource_name] += "    {\n"
            controller_code[resource_name] += f"        {resource_name.capitalize()}::findOrFail($id)->update($request->all());\n"
            controller_code[resource_name] += f"        return response()->json({resource_name.capitalize()}::find($id));\n"
            controller_code[resource_name] += "    }\n\n"
        if permissions.get('DELETE', True):
            controller_code[resource_name] += f"    public function destroy($id)\n"
            controller_code[resource_name] += "    {\n"
            controller_code[resource_name] += f"        {resource_name.capitalize()}::findOrFail($id)->delete();\n"
            controller_code[resource_name] += "        return response()->json(null, 204);\n"
            controller_code[resource_name] += "    }\n"
        controller_code[resource_name] += "}\n\n"
    
    # Model
    for resource_name in resources:
        model_code += f"namespace App\\Models;\n\n"
        model_code += "use Illuminate\\Database\\Eloquent\\Model;\n\n"
        model_code += f"class {resource_name.capitalize()} extends Model\n"
        model_code += "{\n"
        model_code += f"    protected $table = '{resources[resource_name]['table']}';\n"
        model_code += f"    protected $fillable = ['*'];\n"
        model_code += "}\n\n"
        
    route_code += "?>"
    model_code += "?>"
    
    return route_code, controller_code, model_code

def write_code_to_file(code, file_path):
    with open(file_path, "w") as file:
        file.write(code)
    print(f"File generated: {file_path}")

project_name = "GeneratedAPI"
print(f"@@@@@@@@@@#P555PB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BBGGGB&@@@@&BBGGGGGG&@@@B5555PB@@GGGGBBGGGGB@@@@")
print(f"@@@@@@@@#~~YPP5J!?@@@@&##&@@@@@@@@@@@@@@@@@&##@@@@@G ^YJJ7^J@@@G ^YYJJJY&@P^!5PP5?~5&YJJJ^ 7YJJP@@@@")
print(f"@@@@@@@@5 ?&@@@@@&@@#!7??7!5@@?~#@@@@77&@G!!?7!7#@@G 7@@@@^ #@@G !&&&&&&@@~ 5@@@@@@&@@@@@! G@@@@@@@@")
print(f"@@@@@@@@@5!~~!!7Y#@@@BGP55^ #@B.~@@@? G@P ?@@@&~.#@G ~55Y7~5@@@G :??????#@#J~~~!!?P&@@@@@! P@@@@@@@@")
print(f"@@@@@@@@@@@@&#BP:.#@J:7Y5P! B@@G 7@Y P@@? G@@@@Y P@G ~PP7 J@@@@G !@@@@@@@@@@@&&#BY ~@@@@@! P@@@@@@@@")
print(f"@@@@@@@@J?PB&&#G^^&&:.B&&B~ B@@@P ! Y@@@B:~G##P:~&@G 7@@@G~:5&@G ~&#####@&?YG#&&#Y.?@@@@@! P@@@@@@@@")
print(f"@@@@@@@@BY?????JP@@@#J7?J5J!#@@@@5~Y@@@@@&5????P@@@B!Y@@@@@5!Y@B!7??????#@PJ?????JB@@@@@@Y!B@@@@@@@@")
print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
response = input(f"\nWelcome to SavoREST Framework! type --help for some tips :)")
if response == '--help':
    print(f"\nHere the commands:")
    print(f"\nCreate <filepath> <projectname> | Create the API REST")
    print(f"\nSyntax                           | View the syntax for create you API")
elif response == 'Syntax':
    print(f"\nView: https://github.com/dylanpatriarchi/SavoREST for file syntax")
else:
    parti = response.split()
    if len(parti) == 3 and parti[0] == "Create":
        file_path = parti[1]
        projectname = parti[2]
        create_lumen_project(projectname)
        os.chdir(projectname)



try:
    with open(file_path, 'r') as file:
        file_content = file.read()
        resources, _ = parse_resources_and_accounts(file_content)

        route_code, controller_code, model_code = generate_lumen_code(resources)

        write_code_to_file(route_code, "routes/web.php")

        for resource_name, controller_code in controller_code.items():
            write_code_to_file(controller_code, f"app/Http/Controllers/{resource_name.capitalize()}Controller.php")
            write_code_to_file(model_code, f"app/Models/{resource_name.capitalize()}.php")

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print("Error in Creation of Lumen Project", e)
