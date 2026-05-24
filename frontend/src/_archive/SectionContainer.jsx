export default function SectionContainer({
                                             title,
                                             children
                                         }) {

    return (

        <div
            style={{
                marginBottom: "20px",
                padding: "16px",
                backgroundColor: "#ffffff",
                borderRadius: "10px"
            }}
        >

            <h2>
                {title}
            </h2>

            {children}

        </div>
    );
}