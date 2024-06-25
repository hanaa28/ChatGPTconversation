from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, Thread
from .serializers import ThreadSerializer, MessageSerializer
from .utils import send_code_to_api

class ChatView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        qs = Thread.objects.filter(user=request.user)
        serializer = ThreadSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy() 
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            input_message = serializer.validated_data['_input']

            # Find or create a thread for the current user
            thread, created = Thread.objects.get_or_create(user=request.user)

            # Get the conversation history
            conversation_history = Message.objects.filter(thread=thread).order_by('created_at')
            conversation_history = list(conversation_history.values('_input', '_output', 'user'))
            conversation_history.append({'_input': input_message, '_output': '', 'user': request.user.id})

            output_message = send_code_to_api(conversation_history)
            print(output_message)

            # Create the message with the thread and output
            code_explainer = Message.objects.create(
                user=request.user,
                _input=input_message,
                _output=output_message,
                thread=thread
            )
            response_serializer = MessageSerializer(code_explainer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


















# from rest_framework import views, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Message
# from .serializers import CodeExplainSerializer
# from .utils import send_code_to_api
# import logging

# logger = logging.getLogger(__name__)

# class CodeExplainView(views.APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         qs = Message.objects.all()
#         serializer = CodeExplainSerializer(qs, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         input_message = request.data.get('_input', '').strip()
        
#         if not input_message:
#             return Response({"detail": "Input cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Retrieve or initialize conversation history from session
#             conversation_history = request.session.get('conversation_history', [])
#             conversation_history.append({'role': 'user', 'content': input_message})

#             # Call utility function with current conversation context
#             output_message = send_code_to_api(conversation_history)
#             print(conversation_history)

#             if output_message:
#                 # Update conversation history in session with assistant's response
#                 request.session['conversation_history'] = conversation_history

#                 # Save message to database
#                 code_explainer = Message.objects.create(
#                     user=request.user,
#                     _input=input_message,
#                     _output=output_message
#                 )
#                 response_serializer = CodeExplainSerializer(code_explainer)
#                 return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"detail": "Failed to get a response from the API."}, status=status.HTTP_502_BAD_GATEWAY)
        
#         except Exception as e:
#             logger.error(f"Error sending code to API: {e}")
#             return Response({"detail": "An error occurred while processing your request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#         return Response({"detail": "Failed to process the request."}, status=status.HTTP_400_BAD_REQUEST)

