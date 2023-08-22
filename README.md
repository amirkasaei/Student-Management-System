# Student-Management-System


## Purpose
- In this project, we will create a program to save students' information using **hashing** techniques and and **trie tree**.
- This project was done for the Data Structure Course at **University of Guilan** in 2021 May 

## Description
### The program has the following processes:
  1. Student registration: The student's details, including first and last name, student number, average and major, are taken and the student is added to the program.
  2. Searching for a student: after searching for a student based on the student number, he/she can do the following operations:
     - View profile
     -  delete
     -  Editing
     
  ### A student class includes:
  1. Name and  Surname
  2. Student number
  3. Rate
  4. String
  After a student object is created, it is hashed and stored in the data structure or associated with the hash.

 ### Data Structures:
 1. **Hashing:**
    - A suitable hashing algorithm has been implemented. This algorithm considers a hash key for each student object, with which we can access the student object.
 3. **Trie tree:**
    - To optimize the search, a tree of ideas is implemented based on the student number and the hash key corresponding to the desired student number is stored in the node.
    - In computer science, a trie, also called digital tree or prefix tree, is a type of k-ary search tree, a tree data structure used for locating specific keys from within a set.
### GUI:
- The graphic UI is implemented using PyQt5
  <div align="center"><img src="https://github.com/amirkasaei/Student-Management-System/blob/main/img/ui.png?raw=true" width="40%" /></div>

## Contributors
- Amir Kasaei
- Amir Ezzati
