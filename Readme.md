# GhibliPlay

GhibliPlay is a web-based application which helps to track new films of Ghibli Studio.

After setup and run, the application will answer on HTTP-Requests by the address
`http://localhost:5000/movies` and show full list of the movies and their stars!


## Requirements

* Python >= 3.7
* Pip

## Usage

Before running the application we need to create virtual environment:
```bash
$ make env
```

activate it:
```bash
$ source .env/bin/activate
```

and that's it!

For normal usage simply run
```bash
$ make run-production
```

If it's something wrong with the execution or you want to improve existing codebase then you
need to run the application in development mode:
```bash
$ make run-development
```

If you need to run tests use `make test`


## Author

Petr Orlov <zfmeze@gmail.com>

## License

GhibliPlay is distributed under the GNU GPL3 License. See [LICENSE](LICENSE) file for details.
