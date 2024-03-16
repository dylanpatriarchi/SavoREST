# SavoREST Framework

SavoREST is a lightweight framework for creating RESTful APIs in Lumen. It is designed to be easy to use and flexible, allowing developers to quickly build robust APIs for their projects.

## Key Features

- **Simplicity:** Get started with creating APIs in just a few simple steps.
- **Flexibility:** Customize your endpoints to suit the specific requirements of your project.
- **HTTP Request Handling:** Easily manage HTTP GET, POST, PUT, and DELETE requests.
- **Data Serialization:** Automatic serialization and deserialization of JSON data.

## Getting Started

To get started with SavoREST, follow these steps:

1. Clone the repository `pip install savorest`.
2. Create you file .rrest by defining endpoints using SavoREST's intuitive syntax, in the next section i'll explain the Syntax.
3. Start your SavoREST with 
```bash
python index.py
```
4. Digit 
```bash 
Create path/to/your/file/.rrest Name_project
``` 
and see the result!

## Syntax

It's easy, here an example:
```
resources{
    define_resource: name_resource1 ['CREATE' = true, 'POST' = true, 'UPDATE' = true, 'DELETE' = true] && uri && dbtable
    define_resource: name_resource2 ['CREATE' = false, 'POST' = true, 'UPDATE' = true, 'DELETE' = false] && uri && dbtable
    define_resource: name_resource3 ['CREATE' = false, 'POST' = true, 'UPDATE' = true, 'DELETE' = false] && uri && dbtable
}
```

## IMPORTANT

The project is in beta phase, for bug reporting please report to [info@patriarchidylan.it](mailto:info@patriarchidylan.it)

## Contributing

We welcome contributions from the community! If you'd like to contribute to SavoREST, please follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

SavoREST is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact [info@patriarchidylan.it](mailto:info@patriarchidylan.it).
