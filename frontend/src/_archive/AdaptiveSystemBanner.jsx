export default function AdaptiveSystemBanner({
                                                 message
                                             }) {

    return (

        <div
            style={{
                padding: "14px",
                marginBottom: "20px",
                backgroundColor: "#e5e7eb",
                borderRadius: "10px"
            }}
        >

            <p>
                {message}
            </p>

        </div>
    );
}