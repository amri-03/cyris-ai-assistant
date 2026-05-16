export default function ValidationStatusCard({
                                                 validationStatus
                                             }) {

    return (

        <div>

            <h3>
                Validation Status
            </h3>

            <p>
                {validationStatus}
            </p>

        </div>
    );
}