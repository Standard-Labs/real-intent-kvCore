import streamlit as st
import pandas as pd


# Define global variables for column mappings
COLUMN_MAPPINGS = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "email_1": "Email",
    "email_2": "second email",
    "email_3": "Spouse Email",
    "phone_1": "Cell Phone 1",
    "phone_2": "Cell Phone 2",
    "phone_3": "Home Phone",
    "address": "Primary Address",
    "city": "Primary City",
    "state": "Primary State",
    "zip_code": "Primary Zip",
}


def main():
    st.title('Real Intent to kvCore Converter')

    st.info("""
    Upload a CSV file. The app will convert your Real Intent CSV into a format that can be imported into kvCore.
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    hashtag = st.text_input("(Optional) Enter a hashtag(s). For multiple hashtags, separate them with a '|' with no spaces.")
    st.write("For example: Barrington|Naperville")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Check if required columns are in the dataframe
        missing_columns = [col for col in COLUMN_MAPPINGS.keys() if col not in df.columns]
        
        if not missing_columns:

            df_filtered = df[list(COLUMN_MAPPINGS.keys())].rename(columns=COLUMN_MAPPINGS)


            df['Agent Notes'] = ''

            if 'household_income' in df.columns:
                df_filtered['Agent Notes'] = df['household_income'].apply(lambda x: f"Household Income: {x}")
            
            if 'household_net_worth' in df.columns:
                df_filtered['Agent Notes'] = df_filtered['Agent Notes'] + df['household_net_worth'].apply(lambda x: f", Net Worth: {x}")

            if 'insight' in df.columns:
                df_filtered['Agent Notes'] = df_filtered['Agent Notes'] + df['insight'].apply(lambda x: f", Insight: {x}")


                df = df_filtered
                df['Referrer'] = 'Real Intent'
                df['Source'] = 'Real Intent'
                
                if hashtag:
                    df["Hashtag"] = hashtag

                # Display the resulting dataframe
                st.write("Converted DataFrame:")
                st.write(df)
                
                # Download the converted dataframe as CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download converted CSV",
                    data=csv,
                    file_name='converted_file.csv',
                    mime='text/csv',
                )
        else:
            st.write(f"The uploaded file does not contain the required columns: {', '.join(missing_columns)}.")


if __name__ == "__main__":
    main()