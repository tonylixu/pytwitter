from django import forms


from .models import Tweet

MAX_TWEET_LENGTH = 240

class TweetForm(forms.ModelForm):
    # Meta class to describe the form itself
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        """
        Make sure tweet content is less than MAX_TWEET_LENGTH

        Raises:
            forms.ValidationError: _description_

        Returns:
            _type_: _description_
        """
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content
