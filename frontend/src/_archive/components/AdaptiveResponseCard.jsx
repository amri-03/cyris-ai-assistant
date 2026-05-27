export default function AdaptiveResponseCard({
                                                 response
                                             }) {

    return (

        <div
            style={{
                padding: "14px",
                marginBottom: "12px",
                backgroundColor: "#f4f4f5",
                borderRadius: "8px"
            }}
        >

            <p>
                {response}
            </p>

        </div>
    );
}