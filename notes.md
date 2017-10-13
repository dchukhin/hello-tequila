The steps that I took to set up the hello-tequila project:

 - create a virtual environment for the hello-tequila project

     mkvirtualenv --python=`pythonz locate 3.5.1` hello-tequila

 - create a Django project

     django-admin startproject hello_tequila
     createdb --encoding UTF-8 hello_tequila
     echo "DJANGO_SETTINGS_MODULE=hello_tequila.settings.local" >> .env
     python manage.py migrate

   Now I was able to run the Django project with

     python manage.py runserver

 - I talked to Jeff and followed the steps on  https://gist.github.com/jbradberry/162ed6850d62742f44926b5d6e38026d about how to
 set up a project on tequila.

    - I set up the skeleton for the deployment directory:

      hello_tequila/
      └── deployment
          ├── environments
          ├── keys
          └── playbooks

    - I added 1 environment with an inventory file to deployment/environments. Now
      my directory structure looked like:

      hello_tequila/
      └── deployment
          ├── environments
             └── staging
          │       └── inventory
          ├── keys
          └── playbooks

    - I added group_vars/all subdirectories for each environment in
      deployment/environments. Now my directory structure looked like:

      hello_tequila/
      └── deployment
          ├── environments
          |   └── staging
          │   |   ├── inventory
          |   │   └── group_vars
          │   │       └── all
          │   │           ├── secrets.yml
          │   │           └── vars.yml
          ├── keys
          └── playbooks


    - I set up the skeleton for the deployment playbooks. Now my directory
      structure looked like:

      hello_tequila/
      └── deployment
          ├── environments
          |   └── staging
          │   |   ├── inventory
          |   │   └── group_vars
          │   │       └── all
          │   │           ├── secrets.yml
          │   │           └── vars.yml
          ├── keys
          └── playbooks
              └── group_vars
                  └── all
                      ├── devs.yml
                      └── project.yml

    - I added an ansible config file. Now my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |       └── group_vars
      |           └── all
      |               ├── devs.yml
      |               └── project.yml
      └── ansible.cfg

    - I created a .vault_pass file (with a password) and put it at the base
      directory of the project. I made sure to add this file to the .gitignore
      file, so it's never checked into the repository. Now my directory structure
      looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |       └── group_vars
      |           └── all
      |               ├── devs.yml
      |               └── project.yml
      ├── ansible.cfg
      └── .vault_pass

    - I created a requirements.yml file in the deployment/ directory with 5 basic
      roles: tequila-common, tequila-postgresql, tequila-nginx, tequila-django,
      and nodejs:

      ---
      - src: https://github.com/caktus/tequila-common
        version: v0.8.0
        name: tequila-common

      - src: https://github.com/caktus/tequila-postgresql
        version: v0.8.0
        name: tequila-postgresql

      - src: https://github.com/caktus/tequila-nginx
        version: v0.8.4
        name: tequila-nginx

      - src: https://github.com/caktus/tequila-django
        version: v0.9.5
        name: tequila-django

      - src: geerlingguy.nodejs
        version: 4.1.2
        name: nodejs


      Now my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   └── group_vars
      |   |       └── all
      |   |           ├── devs.yml
      |   |           └── project.yml
      |   └── requirements.yml
      ├── ansible.cfg
      └── .vault_pass

    - In order to take a break, I obtained up a server and set up my key on it
      for ssh access. I ran a command to make sure it works:

       ansible all -i deployment/environments/staging/inventory -m raw -a 'echo "hello world"' -u root

      and I got back:

       staging | SUCCESS | rc=0 >>
       hello world

      so it worked!


    # PLAYBOOKS

    - I obtained a copy of playbook files for the following things:
       - bootstrap_python.yml - a playbook to install Python 2 on the server
         (since up-to-date Ubuntu servers don't have Python 2 by default)
       - common.yml - a playbook exercising the tequila-common Ansible role
       - db.yml - a playbook exercising the tequila-postgresql Ansible role
       - web.yml - a playbook exercising the tequila-nginx and tequila-django Ansible roles
       - site.yml - a catch-all playbook that uses the include directive to pull
         in at least the common, db, and web playbooks

      I started putting these into the repository (into deployment/playbooks/)
      one by one, and running them. First, I put bootstrap_python.yml, which
      looked like this:

      # deployment/playbooks/bootstrap_python.yml
      ---
      - hosts: all
        gather_facts: false
        become: true
        tasks:
          - name: install Python 2
            raw: test -e /usr/bin/python || (apt -y update && apt install -y python-minimal)



      into the directory, so my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   ├── group_vars
      |   |   |   └── all
      |   |   |       ├── devs.yml
      |   |   |       └── project.yml
      |   |   └── bootstrap_python.yml
      |   └── requirements.yml
      ├── ansible.cfg
      └── .vault_pass



      and I ran the playbook in order to install python on the server:

       ansible-playbook -i deployment/environments/staging/inventory -u root deployment/playbooks/bootstrap_python.yml

       PLAY ***************************************************************************

       TASK [install Python 2] ********************************************************
       ok: [staging]

       PLAY RECAP *********************************************************************
       staging                    : ok=1    changed=0    unreachable=0    failed=0   



      Next, I put common.yml, which looked like this:
      # deployment/playbooks/common.yml
      ---
        - hosts: web:db:queue:worker:search
          become: yes
          roles:
            - tequila-common

      into the same directory, but before running it, needed to do several things
      (see https://github.com/caktus/tequila-common):

        I installed each of the roles defined in the requirements.yml:

         ansible-galaxy install -r deployment/requirements.yml

        I wanted to run the tequila-common role, but I also needed to define several
        things before doing so:

          - Since tequila-common doesn't define groups, I needed to add groups to
            the inventory file:

            # deployment/environments/staging/inventory
            staging ansible_host=shipit0.caktus-built.com

            [db]
            staging

            [web]
            staging

            [worker]

        - I also needed to add my ssh key to the list of developers in
          deployment/playbooks/group_vars/all/devs.yml:

          # deployment/playbooks/group_vars/all/devs.yml:
          users:
            - name: dchukhin
              public_keys:
                - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDCyaAGW8HiLvLP9whINKHck0faKwryO++lqA+GYD9G2XZkbsxcBKqU1b3STGn8jXrDjtr4FcKXFGLq8uOS4/FOiCs45TwLOcA4enyTbaPxrZA05Zw5J5hYZ1y4bBvc+GxytAoyySN3MTG7Q2Mb3TgTTl5G/J+d+zGljHBbrjn1Y3xCRPi9ed82bzqdI+6S8kk7kzub++EScjegTfbPhtsyrY4WbZ0Z/hW0Odtt4rXhsktdfLpYTZ3jJs9YapOBFHblRRlZxtc45o5Q2+4B8z8dr1t3jiFqJJdTL5Cnn+DzD/CHiJE/hT8hc4XcHJPjfymMlX2c6AhxN87RcOWHplTGirkNwSnsyquM4fzZPlXpR7aPbTXQNjGrryk95EEkes+/RmdES6QCptGCqGtcmCRFvIYh4v50r7OvyU12GJUmN3HWyDcLMY6JmDvfYzz2ETBeMPWVP++N4IVDzG08WenjA4vTkw2Yvwaodbhe8m0vodqfkNX/ll13wMKf6TAKLFOLc8NfRh4xP936d4xL7pcsGS6LC6pVd6JjJ3CKKHqGcxRuw/00IzFoRRgs+fzIhmXUKbrFtAJbkXaYpV/rfzRc+no3ddWwZ4hK0FaQ5YBU1rfkCBoJzzIWFdJc8dqfbSMwMohHtFZGDhX9seJoo5KZFUbzl0qSD2hJrehGB3k3fQ== dchukhin@gmail.com"


        - Since tequila-common checks the env_name variable, I needed to add that
          variable to the staging variables in
          deployment/environments/staging/group_vars/all/vars.yml:

          # deployment/environments/staging/group_vars/all/vars.yml
          env_name: 'staging'

      At this point my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   ├── group_vars
      |   |   |   └── all
      |   |   |       ├── devs.yml
      |   |   |       └── project.yml
      |   |   ├── bootstrap_python.yml
      |   |   └── common.yml
      |   └── requirements.yml
      ├── ansible.cfg
      └── .vault_pass


      Now I was ready to run the tequila-common role:

       ansible-playbook -i deployment/environments/staging/inventory -u root deployment/playbooks/common.yml


       PLAY RECAP *********************************************************************
       staging                    : ok=23   changed=11   unreachable=0    failed=0  


      Success!

      Next, I moved on to db.yml:

       # deployment/playbooks/db.yml
       ---
       - hosts: db
         become: yes
         roles:
         - tequila-postgresql

      At this point my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   ├── group_vars
      |   |   |   └── all
      |   |   |       ├── devs.yml
      |   |   |       └── project.yml
      |   |   ├── bootstrap_python.yml
      |   |   ├── common.yml
      |   |   └── db.yml
      |   └── requirements.yml
      ├── ansible.cfg
      └── .vault_pass

      The db.yml role requires several more variables (see
      https://github.com/caktus/tequila-nginx), so I defined them in
      deployment/environments/staging/group_vars/all/vars.yml:

       # deployment/environments/staging/group_vars/all/vars.yml
       env_name: 'staging'
       db_name: 'hello_tequila_staging'
       db_user: 'hello_tequila_staging'
       pg_version: 9.5
       app_minions: "{{ groups['web'] | union(groups['worker']) }}"

      The app_minions come from the groups I previously defined in the deployment/environments/staging/inventory file

      Also, I added the db_password to the
      deployment/environments/staging/group_vars/all/secrets.yml. Also, in order
      to not forget the keys in the secrets files, I reference it in the
      deployment/environments/staging/group_vars/all/vars.yml:

       # deployment/environments/staging/group_vars/all/secrets.yml
       SECRET_DB_PASSWORD: '<my database password here>'

       # deployment/environments/staging/group_vars/all/vars.yml
       env_name: 'staging'
       db_name: 'hello_tequila_staging'
       db_user: 'hello_tequila_staging'
       db_password: '{{ SECRET_DB_PASSWORD }}'
       pg_version: 9.5
       app_minions: "{{ groups['web'] | union(groups['worker']) }}"

      Since I now have secrets, I need to encrypt them, so I ran the command to
      do that:

       ansible-vault encrypt deployment/environments/staging/group_vars/all/secrets.yml


       Now I was ready to run the tequila-postgresql role. Because tequila-common
       created a user for me, I no longer had to run the command as root, so I
       ran it as myself:

        ansible-playbook -i deployment/environments/staging/inventory deployment/playbooks/db.yml

        PLAY RECAP *********************************************************************
        staging                    : ok=11   changed=8    unreachable=0    failed=0   

      Success!

      Next, I moved on to web.yml:

       # deployment/playbooks/web.yml
       ---
       - hosts: web
         become: yes
         roles:
           - tequila-nginx
           - { role: tequila-django, is_web: true }
           - nodejs


      At this point my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   ├── group_vars
      |   |   |   └── all
      |   |   |       ├── devs.yml
      |   |   |       └── project.yml
      |   |   ├── bootstrap_python.yml
      |   |   ├── common.yml
      |   |   ├── db.yml
      |   |   └── web.yml
      |   └── requirements.yml
      ├── ansible.cfg
      └── .vault_pass

      The web.yml role requires a Github deploy key, so I had to create one:

        - I created a Makefile at the project root:

        # Makefile
        PROJECT_NAME = hello_tequila
        STATIC_LIBS_DIR = ./$(PROJECT_NAME)/static/libs

        default: lint test

        test:
        	# Run all tests and report coverage
        	# Requires coverage
        	python manage.py makemigrations --dry-run | grep 'No changes detected' || \
        		(echo 'There are changes which require migrations.' && exit 1)
        	coverage run manage.py test --keepdb
        	coverage report -m --fail-under 98
        	npm test

        lint-py:
        	# Check for Python formatting issues
        	# Requires flake8
        	flake8 .

        lint-js:
        	# Check JS for any problems
        	# Requires jshint
        	./node_modules/.bin/eslint -c .eslintrc "${STATIC_LIBS_DIR}*" --ext js,jsx

        lint: lint-py lint-js

        $(STATIC_LIBS_DIR):
        	mkdir -p $@

        update-static-libs: $(LIBS)

        # Generate a random string of desired length
        generate-secret: length = 32
        generate-secret:
        	@strings /dev/urandom | grep -o '[[:alnum:]]' | head -n $(length) | tr -d '\n'; echo

        deployment/keys/%.pub.ssh:
        	# Generate SSH deploy key for a given environment
        	ssh-keygen -t rsa -b 4096 -f $*.priv -C "$*@${PROJECT_NAME}"
        	@mv $*.priv.pub $@

        staging-deploy-key: deployment/keys/staging.pub.ssh

        production-deploy-key: deployment/keys/production.pub.ssh

        # Translation helpers
        makemessages:
        	# Extract English messages from our source code
        	python manage.py makemessages --ignore 'deployment/*' --ignore 'docs/*' --ignore 'requirements/*' \
        		--no-location --no-obsolete -l en

        compilemessages:
        	# Compile PO files into the MO files that Django will use at runtime
        	python manage.py compilemessages

        pushmessages:
        	# Upload the latest English PO file to Transifex
        	tx push -s

        pullmessages:
        	# Pull the latest translated PO files from Transifex
        	tx pull -af

        setup:
        	virtualenv -p `which python3.5` $(WORKON_HOME)/hello_tequila
        	$(WORKON_HOME)/hello_tequila/bin/pip install -U pip wheel
        	$(WORKON_HOME)/hello_tequila/bin/pip install -Ur requirements/dev.txt
        	$(WORKON_HOME)/hello_tequila/bin/pip freeze
        	npm install
        	npm update
        	cp hello_tequila/settings/local.example.py hello_tequila/settings/local.py
        	echo "DJANGO_SETTINGS_MODULE=hello_tequila.settings.local" > .env
        	createdb -E UTF-8 hello_tequila
        	$(WORKON_HOME)/hello_tequila/bin/python manage.py migrate
        	if [ -e project.travis.yml ] ; then mv project.travis.yml .travis.yml; fi
        	@echo
        	@echo "The hello_tequila project is now setup on your machine."
        	@echo "Run the following commands to activate the virtual environment and run the"
        	@echo "development server:"
        	@echo
        	@echo "	workon hello_tequila"
        	@echo "	npm run dev"

        update:
        	$(WORKON_HOME)/hello_tequila/bin/pip install -U -r requirements/dev.txt
        	npm install
        	npm update

        # Build documentation
        docs:
        	cd docs && make html

        .PHONY: default test lint lint-py lint-js generate-secret makemessages \
        		pushmessages pullmessages compilemessages docs

        .PRECIOUS: deployment/keys/%.pub.ssh

        Now my directory structure looked like this:

        hello_tequila/
        └── deployment
        |   ├── environments
        |   |   └── staging
        |   │   |   ├── inventory
        |   |   │   └── group_vars
        |   │   │       └── all
        |   │   │           ├── secrets.yml
        |   │   │           └── vars.yml
        |   ├── keys
        |   └── playbooks
        |   |   ├── group_vars
        |   |   |   └── all
        |   |   |       ├── devs.yml
        |   |   |       └── project.yml
        |   |   ├── bootstrap_python.yml
        |   |   ├── common.yml
        |   |   ├── db.yml
        |   |   └── web.yml
        |   └── requirements.yml
        ├── ansible.cfg
        ├── Makefile
        └── .vault_pass

      I used the Makefile to create a Github deploy key:

       make staging-deploy-key

      This created a private key (staging.priv) at the root of the project, and
      a public key at deployment/keys/staging.pub.ssh.

      I went to the Github repository and added the public key into the "Deploy keys"
      setting under the title "staging".

      Next, I added the private deploy key into the deployment/environments/staging/group_vars/all/secrets.yml file:

       # deployment/environments/staging/group_vars/all/secrets.yml
       SECRET_DB_PASSWORD: '<my database password here>'
       SECRET_GITHUB_DEPLOY_KEY: |
         '<my private github deploy key here>'

      The web.yml role also requires several more variables (see
      https://github.com/caktus/tequila-nginx and
      https://github.com/caktus/tequila-django), so I defined them in deployment/environments/staging/group_vars/all/vars.yml:

       # deployment/environments/staging/group_vars/all/vars.yml
       env_name: 'staging'
       db_name: 'hello_tequila_staging'
       db_user: 'hello_tequila_staging'
       db_password: '{{ SECRET_DB_PASSWORD }}'
       pg_version: 9.5
       app_minions: "{{ groups['web'] | union(groups['worker']) }}"
       domain: 'shipit0.caktus-built.com'
       cert_source: 'none'
       gunicorn_num_workers = 1

      and in deployment/playbooks/group_vars/all/project.yml

       # deployment/playbooks/group_vars/all/project.yml
       project_name: 'hello_tequila'
       repo:
         url: https://github.com/dchukhin/hello-tequila
         branch: master
       force_ssl: false

      also, I needed to add the secret_key, so I added it to secrets.yml and project.yml:

       # deployment/environments/staging/group_vars/all/secrets.yml
       SECRET_DB_PASSWORD: '<my database password here>'
       SECRET_KEY: '<my secret key here>'
       SECRET_GITHUB_DEPLOY_KEY: |
         '<my private github deploy key here>'

       # deployment/playbooks/group_vars/all/project.yml
       project_name: 'hello_tequila'
       repo:
         url: https://github.com/dchukhin/hello-tequila
         branch: master
       force_ssl: false
       secret_key: '{{ SECRET_KEY }}'
       github_deploy_key: '{{ SECRET_GITHUB_DEPLOY_KEY }}'

      I made sure to encrypt the deployment/environments/staging/group_vars/all/secrets.yml.

      I was now ready for the web.yml playbook, so I ran the command:

       ansible-playbook -i deployment/environments/staging/inventory deployment/playbooks/web.yml

       PLAY RECAP **********************************************************************************************************************************************
       staging                    : ok=53   changed=12   unreachable=0    failed=0

      success!

      Next, I added deployment/playbooks/site.yml, which only runs all of the
      other playbooks:

      # deployment/playbooks/site.yml
      ---
      - include: common.yml
      - include: db.yml
      - include: web.yml

      Now my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   ├── group_vars
      |   |   |   └── all
      |   |   |       ├── devs.yml
      |   |   |       └── project.yml
      |   |   ├── bootstrap_python.yml
      |   |   ├── common.yml
      |   |   ├── db.yml
      |   |   ├── site.yml
      |   |   └── web.yml
      |   └── requirements.yml
      ├── ansible.cfg
      ├── Makefile
      └── .vault_pass



    - I added a package.json
      {
        "name": "hello-tequila",
        "devDependencies": {
        }
      }

      Now my directory structure looked like this:

      hello_tequila/
      └── deployment
      |   ├── environments
      |   |   └── staging
      |   │   |   ├── inventory
      |   |   │   └── group_vars
      |   │   │       └── all
      |   │   │           ├── secrets.yml
      |   │   │           └── vars.yml
      |   ├── keys
      |   └── playbooks
      |   |   ├── group_vars
      |   |   |   └── all
      |   |   |       ├── devs.yml
      |   |   |       └── project.yml
      |   |   ├── bootstrap_python.yml
      |   |   ├── common.yml
      |   |   ├── db.yml
      |   |   ├── site.yml
      |   |   └── web.yml
      |   └── requirements.yml
      ├── ansible.cfg
      ├── Makefile
      ├── package.json
      └── .vault_pass


      running the site.yml playbook succeeds with:

       ansible-playbook -i deployment/environments/staging/inventory deployment/playbooks/site.yml

       PLAY RECAP **********************************************************************************************************************************************
       staging                    : ok=84   changed=7    unreachable=0    failed=0   
