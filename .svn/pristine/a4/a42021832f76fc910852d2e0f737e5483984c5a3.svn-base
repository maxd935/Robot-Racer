#!/bin/bash

# création du jar executable
mvn clean compile assembly:single

# création de la doc
mvn javadoc:javadoc

# compilation / execution
mvn clean javafx:run
