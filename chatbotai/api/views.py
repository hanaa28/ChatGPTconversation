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

