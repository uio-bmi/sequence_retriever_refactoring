# Excercise 1
Refactor / clean up the code

# Ecercise 2
Add caching. When fetch_sequence_from_web_service is called, we ideally want it to cache the resulting sequence to a file. 
The next time the function is called with the same parameters, we want to read the cached sequence from file and return that sequence
instead of querying the web service againn.
