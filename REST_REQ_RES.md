# Request objects
REST Request object extends the regular HttpRequest, use to get data from **request.data** similar to request.POST.
```
request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
```

# Response objects
REST Response object, which is a type of TemplateResponse that takes unrendered content and uses content negotiation to
determine the correct content type to return to the client.
```
return Response(data)  # Renders to content type as requested by the client.
```

## STATUS CODE
REST framework provides more explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST in the status module.
It's a good idea to use these throughout rather than using numeric identifiers.

## Wrapping API Views
REST framework provides two wrappers you can use to write API views.
1. The @api_view decorator for working with function based views.
2. The APIView class for working with class-based views.
Wrapper provide request in your view and add context to rsponse obj. The wrappers also provide behaviour such as returning
405 Method Not Allowed responses when appropriate, and handling any ParseError exception that occurs when accessing 
request.data with malformed input.

```
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
request.data can handle incoming json requests, but it can also handle other formats. Similarly we're returning response objects with data, but allowing REST framework to render the response into the correct content type for us.



