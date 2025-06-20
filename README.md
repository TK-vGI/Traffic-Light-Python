# Traffic-Light-Python
By the end of this project, in addition to creating your own "traffic light", you will learn how to work with multi-threading, handle exceptions, inherit classes, and implement and apply the circular queue data structure.
In this project, we will implement a simplified version of such a system for a road junction in which many roads converge to one.

## Stages
1. Output the simple list of options as a control panel for a future traffic light.
2. Good traffic light knows how many roads it controls and the interval between the opening and closing of the road. Input these two values to a program and implement the looped menu's option selection with simple stubs.
3. What if the user inputs "Hello" as the number of roads? The program will terminate with an exception, but the good traffic light should not stop working because of the user's mistake.   Handle it and print the appropriate feedback.
4. Let's continue working with our menu. When the initial settings are provided, create a new thread that will start counting the seconds.
5. Let's give users the option to add and delete new roads. Roads open in a cyclical order, so don't forget to implement the circular queue as a buffer to store elements.
6. Our traffic light doesn't work as expected; it only shows the information about roads that were added to a road junction. Each time the system updates the output, calculate the exact time to close/open for each road.


Link to Hyperskill project: [https://hyperskill.org/projects/351](https://)